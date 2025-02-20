from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def gardenpage(request):

    return render(request, "garden.html")