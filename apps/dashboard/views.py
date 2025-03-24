# Author: Ethan Clapham
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

# Dashboard view
@login_required
def dashboard(request):
    """Loads the dashboard template"""

    return render(request, "dashboard.html")