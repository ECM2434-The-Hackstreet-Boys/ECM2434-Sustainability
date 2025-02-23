# login/urls.py
from django.urls import path
from . import views

# URL patterns for the dashboard app dashboard/
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
