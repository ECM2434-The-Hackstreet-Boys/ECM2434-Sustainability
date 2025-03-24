"""
Views for the QR Scanner app

@Author: Sandy Hay
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Loads QR scan page
@login_required
def qr_scan_view(request):
    """Renders the QR Scanner template"""
    return render(request, 'qr_scan.html')
