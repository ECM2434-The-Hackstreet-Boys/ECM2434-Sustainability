# Author: Matt McCree
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import QuizLocation
from ..recycling.models import Bin
from django.http import JsonResponse


# Loads the play screen
@login_required
def play_screen(request):
    return render(request, 'play_screen.html')


# Loads the map view
@login_required
def map_view(request):
    return render(request, 'map.html')

def get_locations(request):
    quizzes = QuizLocation.objects.all()
    bins = Bin.objects.all()

    quiz_data = [
        {
            'locationName': quiz.locationName,
            'coordinates': [quiz.latitude, quiz.longitude],
            'quizID': quiz.quizID
        } for quiz in quizzes
    ]

    bin_data = [
        {
            'coordinates': [bin.latitude, bin.longitude],
        } for bin in bins
    ]

    return JsonResponse({'quiz_data': quiz_data, 'bin_data': bin_data})
