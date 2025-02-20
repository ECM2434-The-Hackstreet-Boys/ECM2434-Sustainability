from django.urls import path
from . import views

urlpatterns = [
    path('', views.mygardenpage, name='mygarden'),
]