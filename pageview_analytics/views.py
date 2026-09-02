import json

from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from pageview_analytics import config, stats, tracking

# Generous on purpose: a real visitor's own tab can legitimately fire several
# of these (visibility toggles, the once-a-minute safety net, multiple tabs),
# this is only meant to catch someone hammering the endpoint outright. Kept
# self-contained (not website.utils.rate_limited) so this app has no
# dependency on the host project -- see the module docstring in models.py.
_BEACON_LIMIT = 60
_BEACON_WINDOW_SECONDS = 300


def _beacon_rate_limited(request):
    key = f'pva_beacon_{tracking.client_ip(request)}'
    attempts = cache.get(key, 0)
    if attempts >= _BEACON_LIMIT:
        return True
    cache.set(key, attempts + 1, timeout=_BEACON_WINDOW_SECONDS)
    return False


@csrf_exempt
@require_POST
def duration_beacon(request):
    """Receives {vid, seconds} from analytics.js via sendBeacon/XHR. No CSRF
    token (sendBeacon can't attach one) and no auth -- same as the PHP
    original's pageview.php, this only ever writes a duration against a
    visit_id that a real page view already created, so there's nothing here
    for a stray POST to forge beyond noise."""
    if _beacon_rate_limited(request):
        return HttpResponse(status=429)

    try:
        payload = json.loads(request.body or b'{}')
    except ValueError:
        return HttpResponseBadRequest()

    vid = payload.get('vid')
    seconds = payload.get('seconds')
    if not isinstance(vid, str) or not isinstance(seconds, (int, float)):
        return HttpResponseBadRequest()

    tracking.record_duration(vid, seconds)
    return HttpResponse(status=204)


@staff_member_required
def dashboard(request):
    """The stats.php equivalent. Gated to staff rather than left at an
    unguessable URL -- unlike a static PHP site, this app has real auth
    sitting right there, so there's no reason not to use it."""
    days = int(request.GET.get('days', 30))
    data = stats.build_dashboard(days=days, site_hosts=config.get('SITE_HOSTS'))
    data['home_url'] = config.get('HOME_URL')
    return render(request, 'pageview_analytics/dashboard.html', data)
