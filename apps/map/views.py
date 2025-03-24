"""
Views for the map page

@author: Matt McCree
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def map(request):
    """
    Renders the map template
    
    The map shows:
    - Your Location
    - Ecostop Locations
    - Bin Locations
    """
    return render(request, "map.html")

# Create your views here.
