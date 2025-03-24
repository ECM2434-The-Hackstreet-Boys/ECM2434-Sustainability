"""
Views for the home page

@Author: Ethan Clapham
"""
from django.shortcuts import render

# Create your views here.

# Homepage view
def homepage(request):
    """Renders the homepage view template"""
    return render(request, "home.html")