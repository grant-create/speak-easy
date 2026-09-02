"""Aggregation queries for the dashboard. Kept separate from views.py so the
numbers can be reused (a management command, an API, a test) without going
through a Django view.

The one thing that has to happen "in one place, before any figure is
derived" (same rule the PHP version follows): excluding datacentre traffic.
Every function below starts from visitor_and_datacenter_querysets() rather
than filtering its own copy of the rule.
"""
import datetime
from collections import Counter
from urllib.parse import urlparse

from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from pageview_analytics import config, geoip
from pageview_analytics.models import LoginEvent, PageView, VisitorLocation


def _datacenter_location_ids():
    return [loc.id for loc in VisitorLocation.objects.all() if loc.is_datacenter()]


def visitor_and_datacenter_querysets(since=None):
    """Split page views into (real visitors, datacentre traffic). An address
    with no location yet counts as a visitor -- guessing "datacentre" for an
    unresolved lookup would hide a real person from every figure; guessing
    "visitor" only leaves a scraper on screen until it resolves."""
    qs = PageView.objects.all()
    if since is not None:
        qs = qs.filter(created_at__gte=since)

    dc_ids = _datacenter_location_ids()
    if not dc_ids:
        return qs, qs.none()

    return qs.exclude(location_id__in=dc_ids), qs.filter(location_id__in=dc_ids)


def _normalize_host(host):
    host = (host or '').lower()
    if host.startswith('www.'):
        host = host[4:]
    return host


def _referrer_breakdown(visitor_qs, site_hosts):
    """Grouped by host rather than exact URL (so google.com and
    www.google.com are one row), with in-site navigation excluded."""
    site_hosts = {_normalize_host(h) for h in site_hosts}
    counts = Counter()

    for referrer in visitor_qs.exclude(referrer='').values_list('referrer', flat=True):
        host = _normalize_host(urlparse(referrer).netloc)
        if not host or host in site_hosts:
            continue
        counts[host] += 1

    return counts.most_common(50)


def build_dashboard(days=30, site_hosts=(), visitors_limit=200, datacentres_limit=50):
    since = timezone.now() - datetime.timedelta(days=days)
    visitor_qs, datacenter_qs = visitor_and_datacenter_querysets(since)

    total_views = visitor_qs.count()
    unique_visitors = visitor_qs.values('visitor_key').distinct().count()
    avg_seconds = visitor_qs.filter(duration_seconds__isnull=False).aggregate(
        avg=Avg('duration_seconds'),
    )['avg']

    daily = list(
        visitor_qs
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(views=Count('id'), uniques=Count('visitor_key', distinct=True))
        .order_by('-day')
    )

    busiest_pages = list(
        visitor_qs.values('page')
        .annotate(views=Count('id'))
        .order_by('-views')[:50]
    )

    by_country = list(
        visitor_qs.exclude(location__isnull=True)
        .values('location__country')
        .annotate(views=Count('id'))
        .order_by('-views')
    )

    recent_logins = list(
        LoginEvent.objects.filter(created_at__gte=since).select_related('user')[:visitors_limit]
    )

    return {
        'days': days,
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'avg_seconds': round(avg_seconds) if avg_seconds else None,
        'daily': daily,
        'busiest_pages': busiest_pages,
        'referrers': _referrer_breakdown(visitor_qs, site_hosts),
        'by_country': by_country,
        'recent_logins': recent_logins,
        'recent_visitors': list(
            visitor_qs.select_related('location').order_by('-created_at')[:visitors_limit]
        ),
        # Only counts addresses actually waiting on a lookup. A private/
        # internal address (misconfigured IP_HEADER, or traffic that never
        # went through the real client-IP path) will never resolve no
        # matter how long we wait, so it doesn't belong in "pending".
        'unresolved_count': sum(
            1 for ip in visitor_qs.filter(location__isnull=True).values_list('ip_address', flat=True)
            if geoip.is_locatable(ip)
        ),
        'datacenter_recent': list(
            datacenter_qs.select_related('location').order_by('-created_at')[:datacentres_limit]
        ),
        'datacenter_total': datacenter_qs.count(),
    }
