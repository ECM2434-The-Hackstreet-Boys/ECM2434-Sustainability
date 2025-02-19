from django.shortcuts import render

def play_screen(request):
    return render(request, 'play_screen.html')

def map_view(request):
    return render(request, 'map.html')
# Create your views here.
