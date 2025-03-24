"""
App for the quiz

@Author: Edward Pratt
"""
from django.apps import AppConfig

class QuizConfig(AppConfig):
    """Quiz App Configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.quiz'
