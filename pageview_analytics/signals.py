"""Records a LoginEvent on every real sign-in, via Django's own
user_logged_in signal -- fires once per session regardless of how many
requests the login view itself involves, and needs no changes to the
host project's login view."""
import logging

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from pageview_analytics.models import LoginEvent
from pageview_analytics.tracking import client_ip

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def _record_login(sender, request, user, **kwargs):
    try:
        LoginEvent.objects.create(user=user, ip_address=client_ip(request))
    except Exception:
        # A login must never fail because analytics couldn't write a row.
        logger.exception('pageview_analytics: failed to record login for %s', user)
