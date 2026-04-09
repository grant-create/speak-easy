from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('languages/add/', views.add_language, name='add_language'),
    path('languages/switch/<int:language_id>/', views.switch_language, name='switch_language'),
]
