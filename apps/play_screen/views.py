# Author: Matt McCree
from django.shortcuts import render


# Loads the play screen
def play_screen(request):
    return render(request, 'play_screen.html')


# Loads the map view
def map_view(request):
    return render(request, 'map.html')

