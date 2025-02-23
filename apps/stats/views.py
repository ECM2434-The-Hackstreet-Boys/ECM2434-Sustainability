from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

# View for the stats app /stats/
@login_required
def statspage(request):

    return render(request, "statistics.html")
