"""
URLs for the quiz

@Authors: Edward Pratt, Ethan Clapham, Louis Pampin
"""

from django.urls import path
from . import views


# URL patterns for the quiz app /quiz/
urlpatterns = [
    # Path for standard quiz (no location)
    path('', views.quiz_view, name='quiz'),

    # Path for quiz with location
    path('<int:locationID>', views.quiz_view_by_location, name='quiz_location'),
]