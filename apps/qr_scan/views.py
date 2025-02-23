from django.shortcuts import render

def qr_scan_view(request):
    return render(request, 'qr_scan.html')
