"""
App for the leaderboard

@Author: Edward Pratt
"""
from django.apps import AppConfig


class LeaderboardConfig(AppConfig):
    """Leaderboard App Configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.leaderboard'
