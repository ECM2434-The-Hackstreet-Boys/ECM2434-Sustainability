# Author: Sandy Hay
from django.shortcuts import render


# Loads QR scan page
def qr_scan_view(request):
    return render(request, 'qr_scan.html')
