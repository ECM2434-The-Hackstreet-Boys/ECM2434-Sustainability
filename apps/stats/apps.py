"""
App for the stats

@author: Edward Pratt
"""

from django.apps import AppConfig


class StatsConfig(AppConfig):
    """Statistics Configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stats'
