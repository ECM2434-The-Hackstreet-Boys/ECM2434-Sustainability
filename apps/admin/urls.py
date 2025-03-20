# Author: Ethan Clapham
from django.urls import path
from . import views

# URL patterns for the dashboard app dashboard/
urlpatterns = [
    path('', views.admin, name='admin'),
]