from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import apps.stats.models


# Create your views here.
@login_required
def leaderboardpage(request):

    return render(request, "leaderboard.html")

def retrieveStats(request):
    records = apps.stats.models.Stats.objects.all()
    return render(request, "leaderboard.html", {'records': records})