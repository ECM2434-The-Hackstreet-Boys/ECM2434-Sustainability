from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.stats.models import Stats


# Create your views here.
@login_required
def leaderboardpage(request):
    records = Stats.objects.all()
    return render(request, "leaderboard.html", {'records': records})

