from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def statspage(request):

    return render(request, "statistics.html")