"""Drop-in tracking: add 'pageview_analytics.middleware.PageViewTrackingMiddleware'
to MIDDLEWARE and every HTML page in the project is counted automatically --
no per-view or per-template changes needed. This is the one piece of the
original design Django genuinely simplifies: PHP needed a beacon glued onto
every HTML fragment because AJAX-loaded content couldn't run PHP itself;
here every page is already a real server-rendered response, so one
middleware covers all of them.
"""
import logging

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from pageview_analytics import tracking

logger = logging.getLogger(__name__)

_BODY_CLOSE = b'</body>'


class PageViewTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # A page-view counter is a nicety; the site is not. Anything that
        # goes wrong here (DB hiccup, Celery/Redis unreachable, whatever)
        # should cost the analytics for this one view, never the response
        # already sitting in hand.
        try:
            self._maybe_track(request, response)
        except Exception:
            logger.exception('pageview_analytics: tracking failed for %s', request.path)

        return response

    def _maybe_track(self, request, response):
        if request.method != 'GET' or response.status_code != 200:
            return
        if getattr(response, 'streaming', False):
            return
        content_type = response.get('Content-Type', '')
        if not content_type.startswith('text/html'):
            return

        visit_id = tracking.new_visit_id()
        view = tracking.track_visit(request, visit_id)
        if view is None:
            return

        if hasattr(response, 'render') and not getattr(response, 'is_rendered', True):
            response.add_post_render_callback(lambda r: self._inject(r, visit_id))
        else:
            self._inject(response, visit_id)

    def _inject(self, response, visit_id):
        content = response.content
        if _BODY_CLOSE not in content:
            return
        beacon_url = reverse('pageview_analytics:duration_beacon')
        script_url = staticfiles_storage.url('pageview_analytics/analytics.js')
        snippet = _duration_snippet(visit_id, beacon_url, script_url).encode()
        response.content = content.replace(_BODY_CLOSE, snippet + _BODY_CLOSE, 1)
        if response.get('Content-Length') is not None:
            response['Content-Length'] = len(response.content)


def _duration_snippet(visit_id, beacon_url, script_url):
    return (
        '<script>(function(){'
        f'window.__pvaVid="{visit_id}";window.__pvaBeacon="{beacon_url}";'
        'var s=document.createElement("script");'
        f's.src="{script_url}";s.async=true;'
        '(document.body||document.documentElement).appendChild(s);'
        '})();</script>'
    )
