from django.urls import path
from . import views

urlpatterns = [
    path('', views.playpage, name='play'),
]