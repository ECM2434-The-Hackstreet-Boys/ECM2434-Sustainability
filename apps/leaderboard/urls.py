"""
URL for the leaderboardpage
leaderboard/urls.py

@Author: Edward Pratt
"""

from django.urls import path
from . import views


# URL patterns for the leaderboard app
urlpatterns = [
    path('', views.leaderboardpage, name='leaderboardpage'),
]