"""
Views for the Leaderboard

@Authors: Edward Pratt & Ethan Clapham
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.stats.models import Stats


# Create your views here.

# Leaderboard page view, sends all the stats to the template
@login_required
def leaderboardpage(request):
    """Renders the leaderboard on the webpage"""
    records = Stats.objects.all()


    return render(request, "leaderboard.html", {'records': records})

