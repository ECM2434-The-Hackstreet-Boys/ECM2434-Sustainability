# Authors: Edward Pratt, Ethan Clapham

from random import sample

from django.shortcuts import render, redirect
from .models import quiz
from ..stats.models import Stats
from ..accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from random import shuffle


# Function to render the quiz page
@login_required
def quizpage(request):
    return render(request, "quiz.html")



# Function to render the quiz page with the questions and the score
@login_required
def quiz_view(request):

    # Get 5 random questions from the database
    questions = list(quiz.objects.all())
    number_of_questions = len(questions)
    questions = sample(questions, min(5, number_of_questions))

    # Shuffle the options for each question
    for q in questions:
        q.choices = [q.answer, q.other1, q.other2, q.other3]
        shuffle(q.choices)

    score = 0
    incorrect_answers = []

    # Triggered request when the user submits the quiz
    if request.method == "POST":
        correct_count = 0
        print(request.POST)


        # Check if the user's answer is correct by comparing it to the answer in the database
        for key, value in request.POST.items():
            if key.startswith("q"):
                question_id = int(key[1:])
                question = quiz.objects.get(quizID=question_id)

                if value == question.answer:
                    correct_count += 1
                else:
                    incorrect_answers.append({"question": question.question, "your_answer": value, "correct_answer": question.answer})

        # Ensure Stats model stores points correctly
        user = CustomUser.objects.get(id=request.user.id)  # Get user instance
        user_stats, created = Stats.objects.get_or_create(userID=user)  # Fix reference
        user_stats.yourPoints += correct_count  # Increments your Points used in store
        user_stats.yourTotalPoints += correct_count  # Increments your Total Points
        user_stats.save()

        score = correct_count

    # Render the quiz page with the questions and the score on page load
    return render(request, "quiz.html", {"questions": questions, "score": score, "incorrect_answers": incorrect_answers})