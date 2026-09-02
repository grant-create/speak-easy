import hashlib
import ipaddress

from django.conf import settings
from django.db import models
from django.utils import timezone

from pageview_analytics import config


class VisitorLocation(models.Model):
    """One row per IP address ever seen, resolved once and reused forever
    (until it ages out -- see config.GEOIP_MAX_AGE_DAYS). This is what makes
    location lookups free at read time: stats queries only ever join against
    this table, never call the geolocation provider."""

    ip_address = models.GenericIPAddressField(unique=True)

    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    # The provider's own judgement, taken as-is. Not authoritative on its
    # own -- see is_datacenter() below.
    is_hosting = models.BooleanField(default=False)

    # Self-correction: an address the provider flagged as hosting, but whose
    # visit pattern looks human (see promote_if_human_pattern below), is
    # promoted here and stays that way regardless of what the provider says
    # on a later lookup.
    promoted_to_visitor = models.BooleanField(default=False)

    lookup_failed = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['ip_address'])]

    def __str__(self):
        return f'{self.ip_address} ({self.city or self.country or "unresolved"})'

    def is_stale(self):
        if self.resolved_at is None:
            return True
        max_age = timezone.timedelta(days=config.get('GEOIP_MAX_AGE_DAYS'))
        return timezone.now() - self.resolved_at > max_age

    def is_datacenter(self):
        """The one place this decision gets made -- everything downstream
        (dashboard queries, the purge command) calls this rather than
        re-deriving it, so the network overrides and the promotion always
        win the same way everywhere."""
        ip = ipaddress.ip_address(self.ip_address)

        if _ip_in_any(ip, config.get('VISITOR_NETWORKS')):
            return False
        if _ip_in_any(ip, config.get('DATACENTRE_NETWORKS')):
            return True
        if self.promoted_to_visitor:
            return False
        return self.is_hosting

    def promote_if_human_pattern(self):
        """An address the provider calls hosting can still be a real person
        behind a VPN or iCloud Private Relay. The tell isn't "did it report
        a duration" -- a headless browser does that too, but gives itself
        away by reporting the *same* duration every time, since it loads a
        page, waits a fixed interval and closes. A real reader's durations
        vary. So: promote only on more than one reading, not all identical,
        with at least one at or above HUMAN_MIN_SECONDS. Wrongly promoting
        is worse than not promoting -- it puts scraper traffic back into
        figures people rely on -- so this stays conservative on purpose.
        """
        if not config.get('AUTO_PROMOTE_VISITORS') or self.promoted_to_visitor:
            return False

        durations = list(
            PageView.objects
            .filter(location=self, duration_seconds__isnull=False)
            .values_list('duration_seconds', flat=True)
        )
        if len(durations) < 2:
            return False
        if len(set(durations)) < 2:
            return False
        if max(durations) < config.get('HUMAN_MIN_SECONDS'):
            return False

        self.promoted_to_visitor = True
        self.save(update_fields=['promoted_to_visitor'])
        return True


def _ip_in_any(ip, networks):
    for entry in networks:
        entry = entry.strip()
        if not entry:
            continue
        try:
            if '/' in entry:
                if ip in ipaddress.ip_network(entry, strict=False):
                    return True
            elif ip == ipaddress.ip_address(entry):
                return True
        except ValueError:
            continue
    return False


class PageView(models.Model):
    """One row per page view. Deliberately flat and un-aggregated -- with a
    real database behind it, "views for page X on day Y" is just a filtered
    count, not something that needs its own maintained rollup the way the
    original JSON-file version required."""

    visit_id = models.CharField(
        max_length=32, db_index=True,
        help_text='Ties this view to its later duration report. Not a visitor '
                   'identifier -- generated fresh per view, never reused.',
    )
    page = models.CharField(max_length=255, db_index=True)

    ip_address = models.GenericIPAddressField()
    location = models.ForeignKey(
        VisitorLocation, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='page_views',
    )

    referrer = models.URLField(max_length=300, blank=True)
    user_agent = models.CharField(max_length=200, blank=True)

    # md5(ip + user_agent), truncated. Used only to count unique visitors
    # per day (one row per address+browser+day) without needing raw IP
    # comparisons in every query.
    visitor_key = models.CharField(max_length=16, db_index=True)

    duration_seconds = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['page', 'created_at']),
            models.Index(fields=['visitor_key', 'created_at']),
        ]

    def __str__(self):
        return f'{self.page} @ {self.created_at:%Y-%m-%d %H:%M}'

    @staticmethod
    def make_visitor_key(ip_address, user_agent):
        return hashlib.md5(f'{ip_address}|{user_agent}'.encode()).hexdigest()[:16]


class LoginEvent(models.Model):
    """One row per successful sign-in. Deliberately separate from PageView:
    the goal here is just "who showed up and when" -- not the per-page
    browsing detail (referrers, durations, every link clicked) PageView
    tracks for anonymous traffic. Populated by a receiver on Django's
    built-in user_logged_in signal (see apps.py), not the tracking
    middleware, so it fires exactly once per real sign-in regardless of how
    many pages someone visits afterward."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='login_events',
    )
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        indexes = [models.Index(fields=['user', 'created_at'])]
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} @ {self.created_at:%Y-%m-%d %H:%M}'
