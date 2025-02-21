from django.urls import path
from . import views

urlpatterns = [
    path('', views.quizpage, name='quizpage'),
    path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
]