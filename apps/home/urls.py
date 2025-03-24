"""
URL for the home page
login/urls.py

@Author: Edward Pratt"""
from django.urls import path
from . import views


# Url patterns for the home app /home/
urlpatterns = [
    path('', views.homepage, name='home'),
]
