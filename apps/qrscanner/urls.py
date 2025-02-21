from django.urls import path
from .views import QRCodeScan, QRCodeView

urlpatterns = [
    path('qr-generate/', QRCodeView.as_view(), name='qrcode'),
    path('qr-scan/', QRCodeScan.as_view(), name='qrscan'),
]