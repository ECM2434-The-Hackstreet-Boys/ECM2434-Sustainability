from django.urls import path
from . import views

urlpatterns = [
    path('', views.leaderboardpage, name='leaderboardpage'),
]