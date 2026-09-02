"""Core tracking logic -- the Python equivalent of lemni_track_visit().

Server-side, one call per eligible request (see middleware.py). Unlike the
PHP original, Django gives every page its own full request/response cycle,
so there's no "AJAX fragment can't self-report" problem to work around --
one code path covers every page.
"""
import re
import secrets

from pageview_analytics import config, filters
from pageview_analytics.geoip import queue_geolocation
from pageview_analytics.models import PageView, VisitorLocation

_REFERRER_RE = re.compile(r'^https?://', re.IGNORECASE)
_CONTROL_CHARS_RE = re.compile(r'[\x00-\x1f\x7f]')

_SESSION_KEY_PREFIX = 'pva_counted_'


def new_visit_id():
    """A short random id tying a page view to the duration report that
    follows it. Not a visitor identifier -- per view, never reused."""
    return secrets.token_hex(8)


def client_ip(request):
    header = config.get('IP_HEADER')
    if header:
        candidate = request.META.get(header, '')
        if candidate:
            candidate = candidate.split(',')[0].strip()
            if candidate:
                return candidate
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def clean_referrer(referrer):
    if not referrer:
        return ''
    referrer = _CONTROL_CHARS_RE.sub('', referrer)
    if not _REFERRER_RE.match(referrer):
        return ''
    return referrer[:300]


def is_excluded_path(path):
    return any(path.startswith(prefix) for prefix in config.get('EXCLUDE_PATH_PREFIXES'))


def track_visit(request, visit_id):
    """Record one page view for this request, or do nothing if it's a bot,
    an ignored network, an excluded path, or already counted this session.
    Returns the PageView created, or None."""
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ip = client_ip(request)

    if filters.is_bot(user_agent) or filters.is_ignored_ip(ip):
        return None

    page = request.path
    if is_excluded_path(page):
        return None

    # One count per session per page -- a reload or an anchor click doesn't
    # inflate the numbers.
    session_key = _SESSION_KEY_PREFIX + page
    if request.session.get(session_key):
        return None
    request.session[session_key] = True

    location = VisitorLocation.objects.filter(ip_address=ip).first()
    if location is None or location.is_stale():
        try:
            queue_geolocation(ip)
        except Exception:
            pass  # a lookup failure should cost the location, not the page view

    view = PageView.objects.create(
        visit_id=visit_id,
        page=page,
        ip_address=ip,
        location=location,
        referrer=clean_referrer(request.META.get('HTTP_REFERER', '')),
        user_agent=user_agent[:200],
        visitor_key=PageView.make_visitor_key(ip, user_agent),
    )

    return view


def record_duration(visit_id, seconds):
    """Attach a time-on-page report to the view it belongs to. Called by the
    duration beacon once the browser reports back on hide/unload. A tab can
    report more than once (hidden, then closed) -- keep the longest, same as
    the PHP original."""
    seconds = max(0, min(int(seconds), 86400))  # a day is far beyond any real reading time

    view = PageView.objects.filter(visit_id=visit_id).select_related('location').first()
    if view is None:
        return

    if view.duration_seconds is None or seconds > view.duration_seconds:
        view.duration_seconds = seconds
        view.save(update_fields=['duration_seconds'])

    if view.location:
        view.location.promote_if_human_pattern()
