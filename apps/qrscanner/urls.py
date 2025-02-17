from django.urls import path
from .views import QRCodeScan, QRCodeView

urlpatterns = [
    path('qrcode-generate', QRCodeView.as_view(), name='qrcode'),
    path('qrcode-scan', QRCodeScan.as_view(), name='qrscan'),
]