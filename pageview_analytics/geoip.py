import ipaddress
import logging
import threading

import requests
from django.utils import timezone

try:
    from celery import shared_task
except ImportError:
    # Celery is an optional accelerator, not a hard dependency -- a project
    # with no task queue at all still gets working (if less scalable)
    # geolocation via the thread fallback in queue_geolocation() below.
    def shared_task(func):
        return func

from pageview_analytics.models import PageView, VisitorLocation

logger = logging.getLogger(__name__)

# ip-api.com's free endpoint: no signup, no key. Swap this out for a
# different provider by editing this one function -- nothing else needs to
# change, VisitorLocation only cares about the fields returned below.
_LOOKUP_URL = 'http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,hosting'


def is_locatable(ip_address):
    """False for loopback/LAN/link-local -- no geolocation provider can
    place these, so it's not worth a request or a cache entry."""
    try:
        ip = ipaddress.ip_address(ip_address)
    except ValueError:
        return False
    return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast)


def _save_and_backfill(location, update_fields):
    """Save the resolved (or failed) location, then link it onto any
    PageView rows for this IP that were created before the lookup finished
    -- which is the common case, since a brand-new address has no
    VisitorLocation row yet at the moment its first PageView is written.
    Without this, that first view would show as unresolved forever even
    though the lookup succeeded moments later."""
    location.save(update_fields=update_fields)
    PageView.objects.filter(ip_address=location.ip_address, location__isnull=True).update(location=location)


@shared_task
def resolve_location(ip_address):
    """Look up one address and cache it. Called with .delay() from the
    tracking middleware so the visitor never waits on it -- mirrors the
    PHP version's register_shutdown_function trick, but as a proper queued
    task instead of a same-process deferred callback."""
    if not is_locatable(ip_address):
        return

    location, created = VisitorLocation.objects.get_or_create(ip_address=ip_address)
    if not created and not location.is_stale():
        return

    try:
        resp = requests.get(_LOOKUP_URL.format(ip=ip_address), timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        logger.warning('geoip lookup failed for %s: %s', ip_address, e)
        location.lookup_failed = True
        location.resolved_at = timezone.now()
        _save_and_backfill(location, ['lookup_failed', 'resolved_at'])
        return

    if data.get('status') != 'success':
        location.lookup_failed = True
        location.resolved_at = timezone.now()
        _save_and_backfill(location, ['lookup_failed', 'resolved_at'])
        return

    location.country = data.get('country', '') or ''
    location.region = data.get('regionName', '') or ''
    location.city = data.get('city', '') or ''
    location.is_hosting = bool(data.get('hosting', False))
    location.lookup_failed = False
    location.resolved_at = timezone.now()
    _save_and_backfill(location, [
        'country', 'region', 'city', 'is_hosting', 'lookup_failed', 'resolved_at',
    ])


def queue_geolocation(ip_address):
    """Queue a lookup via Celery when a broker is actually reachable,
    otherwise run it on a daemon thread -- covers Celery not installed at
    all (no .delay attribute, see the shared_task fallback above) and
    Celery installed but unconfigured/unreachable (.delay() raises) with
    the same non-blocking fallback either way."""
    if hasattr(resolve_location, 'delay'):
        try:
            resolve_location.delay(ip_address)
            return
        except Exception:
            pass
    threading.Thread(target=resolve_location, args=(ip_address,), daemon=True).start()
