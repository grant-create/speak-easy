from django.urls import path

from . import views

urlpatterns = [
    path('', views.lesson_list, name='lesson_list'),
    path('<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
]
