# Author: Ethan Clapham, Edward Pratt

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

from apps.quiz.models import quiz
from apps.play_screen.models import QuizLocation



# Create your views here.
def superuser_check(user):
    return bool(user.is_authenticated and (user.is_superuser or user.role == 'admin'))

# Dashboard view
@user_passes_test(superuser_check, login_url='/login/')
def adminDashboard(request):

    questions = quiz.objects.filter(locationID = '0').values_list("question", flat=True)
    locations = QuizLocation.objects.values_list("locationName", flat=True)

    if request.method == "POST":
        if "question" in request.POST and "answer" in request.POST:
            # Handle adding a new question
            new_question = quiz(
                question=request.POST["question"],
                answer=request.POST["answer"],
                other1=request.POST["incorrect1"],
                other2=request.POST["incorrect2"],
                other3=request.POST["incorrect3"],
                locationID='0'
            )
            new_question.save()
            return redirect("admin-dashboard")  # Refresh the page

        elif "question" in request.POST:
            # Handle deleting a question
            question_to_delete = request.POST["question"]
            quiz.objects.filter(question=question_to_delete).delete()
            return redirect("admin-dashboard")

        elif "longitude" in request.POST and "latitude" in request.POST and "location_name" in request.POST:
            # Create a new location
            new_location = QuizLocation(
                longitude=request.POST["longitude"],
                latitude=request.POST["latitude"],
                locationName=request.POST["location_name"],
            )
            new_location.save()

            # Loop through 5 questions and save them
            for i in range(1, 6):  # 1 to 5
                question_text = request.POST.get(f"question_{i}")
                answer = request.POST.get(f"answer_{i}")
                incorrect1 = request.POST.get(f"incorrect_{i}_1")
                incorrect2 = request.POST.get(f"incorrect_{i}_2")
                incorrect3 = request.POST.get(f"incorrect_{i}_3")

                if question_text and answer and incorrect1 and incorrect2 and incorrect3:
                    quiz.objects.create(
                        locationID=new_location.locationID,
                        question=question_text,
                        answer=answer,
                        other1=incorrect1,
                        other2=incorrect2,
                        other3=incorrect3,
                    )

        elif "location_name" in request.POST:
            # Handle deleting a location
            location_to_delete = request.POST["location_name"]
            locationID = QuizLocation.objects.get(locationName=location_to_delete).locationID
            quiz.objects.filter(locationID=locationID).delete()
            QuizLocation.objects.filter(locationName=location_to_delete).delete()
            return redirect("admin-dashboard")



    return render(request, "admin.html", {'questions': questions, 'locations': locations})