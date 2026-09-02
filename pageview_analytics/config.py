"""
Central place to read pageview_analytics's settings, all optional.

Everything lives under one dict in the host project's settings.py so the
app works with zero configuration when first dropped into a project:

    PAGEVIEW_ANALYTICS = {
        'IP_HEADER': 'HTTP_CF_CONNECTING_IP',   # only if behind a proxy/CDN
        'IGNORE_NETWORKS': ['15.177.0.0/18'],   # extra CIDRs/IPs to never count
        'VISITOR_NETWORKS': ['203.0.113.5'],    # always real, overrides the hosting flag
        'DATACENTRE_NETWORKS': ['46.173.0.0/16'],  # always datacentre, overrides it back
        'SITE_HOSTS': ['example.com', 'www.example.com'],  # self-referrals to ignore
        'EXCLUDE_PATH_PREFIXES': ['/admin/', '/api/'],  # never tracked
        'HUMAN_MIN_SECONDS': 30,
        'AUTO_PROMOTE_VISITORS': True,
        'HOME_URL': '/',  # "back to site" link on the dashboard
    }
"""
from django.conf import settings

_DEFAULTS = {
    # '' means REMOTE_ADDR (the address the server actually saw, unforgeable).
    # Set to e.g. 'HTTP_CF_CONNECTING_IP' or 'HTTP_X_FORWARDED_FOR' only when
    # this app really does sit behind a reverse proxy/CDN -- those headers
    # are client-supplied, so trusting one when nothing strips it lets any
    # visitor claim whatever address they like.
    'IP_HEADER': '',

    'IGNORE_NETWORKS': [
        # AWS Route 53 health-checkers -- ~180 hits/hour from six locations,
        # relentless enough to bury real traffic if left uncounted.
        '15.177.0.0/18',
        '15.177.108.0/24',
    ],
    'VISITOR_NETWORKS': [],
    'DATACENTRE_NETWORKS': [],

    'SITE_HOSTS': [],

    # Never tracked regardless of everything else. Prefixes are matched
    # against request.path.
    'EXCLUDE_PATH_PREFIXES': [
        '/admin/', '/radmin/', '/static/', '/media/', '/pageview-analytics/',
    ],

    'HUMAN_MIN_SECONDS': 30,
    'AUTO_PROMOTE_VISITORS': True,

    # How long a resolved location is trusted before it's looked up again --
    # addresses get reassigned to different people/places over time.
    'GEOIP_MAX_AGE_DAYS': 90,

    # Plain path, not a Django URL name -- keeps this app from having to
    # know the host project's urls.py at all. Default of '/' works for any
    # project whose homepage is the site root.
    'HOME_URL': '/',
}


def get(key):
    configured = getattr(settings, 'PAGEVIEW_ANALYTICS', {}) or {}
    return configured.get(key, _DEFAULTS[key])
