from django.contrib import admin

from pageview_analytics.models import LoginEvent, PageView, VisitorLocation


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('page', 'ip_address', 'created_at', 'duration_seconds', 'referrer')
    list_filter = ('created_at',)
    search_fields = ('page', 'ip_address', 'referrer', 'visitor_key')
    readonly_fields = [f.name for f in PageView._meta.fields]
    date_hierarchy = 'created_at'


@admin.register(VisitorLocation)
class VisitorLocationAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'city', 'region', 'country', 'is_hosting', 'promoted_to_visitor', 'resolved_at')
    list_filter = ('is_hosting', 'promoted_to_visitor', 'lookup_failed')
    search_fields = ('ip_address', 'city', 'region', 'country')


@admin.register(LoginEvent)
class LoginEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'created_at')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = [f.name for f in LoginEvent._meta.fields]
    date_hierarchy = 'created_at'
