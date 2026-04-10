from django.urls import path

from . import views

urlpatterns = [
    path('', views.lesson_list, name='lesson_list'),
    path('review/', views.review_quiz, name='review_quiz'),
    path('review/complete/', views.review_complete, name='review_complete'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('phrases/<int:phrase_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('<int:lesson_id>/quiz/', views.lesson_quiz, name='lesson_quiz'),
    path('<int:lesson_id>/quiz/complete/', views.quiz_complete, name='quiz_complete'),
]
