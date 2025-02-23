from django.urls import path
from . import views

urlpatterns = [
    path('', views.retrieveStats, name='retrieveStats'),
]