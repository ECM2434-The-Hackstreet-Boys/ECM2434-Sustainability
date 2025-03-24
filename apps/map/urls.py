"""
URLs for the map page

@Author: Matt McCree
"""
from django.urls import path
from . import views

# URL patterns for the map app map/
urlpatterns = [
    path('', views.map, name='map'),
]