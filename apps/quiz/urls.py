from django.urls import path
from . import views


# URL patterns for the quiz app /quiz/
urlpatterns = [
    path('', views.quiz_view, name='quiz'),
]