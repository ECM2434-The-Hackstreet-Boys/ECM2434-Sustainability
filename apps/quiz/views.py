from django.shortcuts import render, redirect
from .models import quiz
from ..stats.models import Stats
from ..accounts.models import CustomUser
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required
def quizpage(request):
    return render(request, "quiz.html")

@login_required
def quiz_view(request):
    questions = quiz.objects.all()
    score = None

    if request.method == "POST":
        correct_count = 0

        for q in questions:
            user_answer = request.POST.get(f"q{q.quizID}")
            if user_answer == q.answer:
                correct_count += 1

        # Ensure Stats model stores points correctly
        user = CustomUser.objects.get(id=request.user.id)  # Get user instance
        user_stats, created = Stats.objects.get_or_create(userID=user)  # Fix reference
        user_stats.yourPoints += correct_count  # Assuming yourPoints stores points
        user_stats.save()

        score = correct_count
    
    return render(request, "quiz.html", {"questions": questions, "score": score})