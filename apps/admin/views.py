# Author: Ethan Clapham, Edward Pratt

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from apps.quiz.models import quiz
from apps.play_screen.models import QuizLocation
from apps.recycling.models import Bin
from apps.garden.models import Block
from apps.garden.forms import BlockForm, EditBlockForm
from apps.accounts.forms import EditUserForm
from apps.accounts.models import CustomUser


# Create your views here.
def superuser_check(user):
    return bool(user.is_authenticated and (user.is_superuser or user.role == 'admin'))

# Dashboard view
@user_passes_test(superuser_check, login_url='/accounts/login/')
def adminDashboard(request):

    questions = quiz.objects.filter(locationID = '0').values_list("question", flat=True)
    locations = QuizLocation.objects.values_list("locationName", flat=True)
    bins = Bin.objects.values_list("binIdentifier", flat=True)
    blocks = Block.objects.all()
    users = CustomUser.objects.all()



    if request.method == "POST":
        form_type = request.POST.get("form_type")

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


        elif "longitude" in request.POST and "latitude" in request.POST and "bin_identifier" in request.POST:
            new_bin = Bin(
                longitude=request.POST["longitude"],
                latitude=request.POST["latitude"],
                binIdentifier=request.POST["bin_identifier"]
            )
            new_bin.save()
            return redirect("admin-dashboard")

        elif "bin_identifier" in request.POST:
            bin_to_delete = request.POST["bin_identifier"]
            Bin.objects.filter(binIdentifier=bin_to_delete).delete()

        # If the POST contains an 'edit_block' identifier, update an existing block
        if request.POST.get("form_type") == "edit_block":
            block = get_object_or_404(Block, blockID=request.POST.get("blockID"))
            form = EditBlockForm(request.POST, instance=block)
            if form.is_valid():
                form.save()
                return redirect("admin-dashboard")
        # Otherwise, if the POST contains an 'add_block' identifier, create a new block
        elif request.POST.get("form_type") == "add_block":
            form = BlockForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("admin-dashboard")

        elif form_type == "edit_user":
            # Handle editing an existing user (role only)
            user_id = request.POST.get("user_id")
            user_obj = get_object_or_404(CustomUser, id=user_id)
            edit_form = EditUserForm(request.POST, instance=user_obj)
            if edit_form.is_valid():
                edit_form.save()  # This updates the user's role
                return redirect("admin-dashboard")

    else:
        form = BlockForm()






    return render(request, "admin.html", {
        'questions': questions,
        'locations': locations,
        'bins': bins,
        'blocks': blocks,
        'block_form': form,
        'users': users
    })