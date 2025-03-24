"""
App for Settings

@Author: Sandy Hay
"""

from django.apps import AppConfig


class SettingsConfig(AppConfig):
    """Settings Configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.settings'
