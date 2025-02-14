from django.urls import path
from . import views

urlpatterns = [
    path('', views.play_screen, name='play_screen'),
    path('map/', views.map_view, name='map'),
]