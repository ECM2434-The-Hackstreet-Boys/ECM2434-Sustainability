# Author: Ethan Clapham

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def superuser_check(user):
    return user.is_authenticated and user.is_superuser

# Dashboard view
@user_passes_test(superuser_check, login_url='/login/')
def adminDashboard(request):

    return render(request, "admin.html")