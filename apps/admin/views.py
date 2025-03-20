# Author: Ethan Clapham

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# Dashboard view
@login_required
def admin(request):

    return render(request, "admin.html")