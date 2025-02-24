# Author: Sandy Hay

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# QR Scan page view, renders the template
@login_required
def qr_scan_view(request):
    return render(request, 'qr_scan.html')
