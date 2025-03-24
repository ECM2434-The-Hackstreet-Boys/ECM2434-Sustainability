"""
URLs for the QR scanner

@Author: Sandy Hay
"""

from django.urls import path, include
from . import views

# URL pattern for the QR Scanner app qr_scan/
urlpatterns = [
    path('', views.qr_scan_view, name='qr_scan'),
]