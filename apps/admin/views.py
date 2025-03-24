"""Views for the admin page

@Author: Ethan Clapham, Edward Pratt
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from apps.quiz.models import quiz
from apps.play_screen.models import QuizLocation
from apps.recycling.models import Bin
from apps.garden.models import Block
from apps.garden.forms import BlockForm, EditBlockForm
from apps.accounts.forms import EditUserForm
from apps.accounts.models import CustomUser


def superuser_check(user):
    """Check if the user is an admin or gamekeeper."""
    return bool(
        user.is_authenticated and
        (user.is_superuser or getattr(user, 'role', None) in ['admin', 'gamekeeper'])
    )

# Dashboard view
@user_passes_test(superuser_check, login_url='/accounts/login/')
def adminDashboard(request):
    """Handle admin dashboard actions like managing quizzes, locations, bins, users, and blocks."""

    questions = quiz.objects.filter(locationID = '0').values_list("question", flat=True)
    locations = QuizLocation.objects.values_list("locationName", flat=True)
    allLocations = QuizLocation.objects.all()
    bins = Bin.objects.values_list("binIdentifier", flat=True)
    blocks = Block.objects.all()
    users = CustomUser.objects.all()
    allBins = Bin.objects.all()



    if request.method == "POST":
        form_type = request.POST.get("form_type")



        if form_type == "edit_location":
            # Editing existing location MUST be before new location creation
            location_id = request.POST.get("location_id")
            location = QuizLocation.objects.get(locationID=location_id)
            location.longitude = request.POST.get("longitude")
            location.latitude = request.POST.get("latitude")
            location.locationName = request.POST.get("location_name")
            location.save()
            return redirect("admin-dashboard")

        elif form_type == 'edit_bin':
            # Editing existing bin (explicit handling)
            bin_id = request.POST.get('bin_id')
            bin_instance = Bin.objects.get(binID=bin_id)
            bin_instance.binIdentifier = request.POST.get('bin_identifier')
            bin_instance.latitude = request.POST.get('latitude')
            bin_instance.longitude = request.POST.get('longitude')
            bin_instance.save()
            return redirect('admin-dashboard')

        elif "question" in request.POST and "answer" in request.POST:
            # Add new question
            new_question = quiz(
                question=request.POST["question"],
                answer=request.POST["answer"],
                other1=request.POST["incorrect1"],
                other2=request.POST["incorrect2"],
                other3=request.POST["incorrect3"],
                locationID='0'
            )
            new_question.save()
            return redirect("admin-dashboard")

        elif "question" in request.POST:
            # Delete existing question
            question_to_delete = request.POST["question"]
            quiz.objects.filter(question=question_to_delete).delete()
            return redirect("admin-dashboard")

        elif "location_name" in request.POST and "longitude" in request.POST and "latitude" in request.POST:
            # Create new location (must be after specific editing condition!)
            new_location = QuizLocation(
                longitude=request.POST["longitude"],
                latitude=request.POST["latitude"],
                locationName=request.POST["location_name"],
            )
            new_location.save()

            # Handle additional quiz questions if provided
            for i in range(1, 6):
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
            return redirect("admin-dashboard")

        elif "location_name" in request.POST:
            # Delete location by name
            location_to_delete = request.POST["location_name"]
            locationID = QuizLocation.objects.get(locationName=location_to_delete).locationID
            quiz.objects.filter(locationID=locationID).delete()
            QuizLocation.objects.filter(locationName=location_to_delete).delete()
            return redirect("admin-dashboard")

        elif "longitude" in request.POST and "latitude" in request.POST and "bin_identifier" in request.POST:
            # Create new bin
            new_bin = Bin(
                longitude=request.POST["longitude"],
                latitude=request.POST["latitude"],
                binIdentifier=request.POST["bin_identifier"]
            )
            new_bin.save()
            return redirect("admin-dashboard")

        elif "bin_identifier" in request.POST:
            # Delete existing bin
            bin_to_delete = request.POST["bin_identifier"]
            Bin.objects.filter(binIdentifier=bin_to_delete).delete()
            return redirect("admin-dashboard")

        elif form_type == "edit_user":
            # Edit user roles
            user_id = request.POST.get("user_id")
            user_obj = get_object_or_404(CustomUser, id=user_id)
            edit_form = EditUserForm(request.POST, instance=user_obj)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("admin-dashboard")

        elif form_type == "edit_block":
            # Update existing block
            block = get_object_or_404(Block, blockID=request.POST.get("blockID"))
            form = EditBlockForm(request.POST, instance=block)
            if form.is_valid():
                form.save()
                return redirect("admin-dashboard")

        elif form_type == "add_block":
            # Create new block
            form = BlockForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("admin-dashboard")

    else:
        form = BlockForm()

    form = BlockForm()
    return render(request, "admin.html", {
        'questions': questions,
        'locations': locations,
        'allLocations': allLocations,
        'bins': bins,
        'blocks': blocks,
        'block_form': form,
        'users': users,
        'allBins': allBins
    })