from django.urls import path

from pageview_analytics import views

app_name = 'pageview_analytics'

urlpatterns = [
    path('pageview-analytics/', views.dashboard, name='dashboard'),
    path('pageview-analytics/beacon/', views.duration_beacon, name='duration_beacon'),
]
