"""
App for the QR Scanner

@Author: Edward Pratt
"""
from django.apps import AppConfig

class QrScannerConfig(AppConfig):
    """Qr Scanner Configuartion"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.qr_scan'
