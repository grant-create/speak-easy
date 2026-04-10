from django.urls import path

from . import views

urlpatterns = [
    path('', views.lesson_list, name='lesson_list'),
    path('<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('<int:lesson_id>/quiz/', views.lesson_quiz, name='lesson_quiz'),
    path('<int:lesson_id>/quiz/complete/', views.quiz_complete, name='quiz_complete'),
]
