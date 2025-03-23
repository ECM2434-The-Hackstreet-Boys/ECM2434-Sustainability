# Author: Matt McCree
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def map(request):

    return render(request, "map.html")

# Create your views here.
