# Author: Ethan Clapham
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


# View to access the recycling page
@login_required
def recyclepage(request):

    return render(request, ecycling.html")