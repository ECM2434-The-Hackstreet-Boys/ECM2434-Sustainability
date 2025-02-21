from django.shortcuts import render, redirect
from .models import quiz
from ..stats.models import Stats
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
    return render(request, "quiz.html", {"questions": questions})

@login_required
def submit_quiz(request):
    if request.method == 'POST':
        correct = 0
        questions = quiz.objects.all()

        for q in questions:
            user_answer = request.POST.get(f"q{q.quizID}")
            if user_answer == q.answer:
                correct += 1
            
        user_stats = Stats.objects.get(user=request.userID)
        user_stats.yourPoints += correct
        user_stats.save()

        return render(request, "quiz_request.html", {"correct": correct, "total": len(questions)})
    return redirect("dashboard")