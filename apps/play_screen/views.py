# Author: Matt McCree
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Loads the play screen
@login_required
def play_screen(request):
    return render(request, 'play_screen.html')


# Loads the map view
@login_required
def map_view(request):
    return render(request, 'map.html')

