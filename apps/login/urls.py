# login/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage, name='login'),
]
