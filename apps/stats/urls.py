from django.urls import path
from . import views


# URL patterns for the stats app
urlpatterns = [
    path('', views.statspage, name='stats'),
]