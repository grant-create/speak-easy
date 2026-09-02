from django.apps import AppConfig


class PageviewAnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pageview_analytics'
    verbose_name = 'Page View Analytics'

    def ready(self):
        # Imported here rather than at module level -- app registry isn't
        # ready yet when apps.py itself is first imported.
        from pageview_analytics import signals  # noqa: F401
