from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.qr_scan_view, name='qr_scan'),
]