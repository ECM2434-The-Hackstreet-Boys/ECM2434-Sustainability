# Author: Ethan Clapham, Edward Pratt

# Import necessary Django utilities and decorators for views and authentication
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

# Import required models and forms from various apps
from apps.quiz.models import quiz
from apps.play_screen.models import QuizLocation
from apps.recycling.models import Bin
from apps.garden.models import Block
from apps.garden.forms import BlockForm, EditBlockForm
from apps.accounts.forms import EditUserForm
from apps.accounts.models import CustomUser


# Utility function to verify user permissions (checks for admin or superuser role)
def superuser_check(user):
    # Returns True if the user is authenticated and is either a superuser or has an admin role
    return bool(user.is_authenticated and (user.is_superuser or user.role == 'admin'))


# Admin dashboard view protected by user role check, redirects unauthorized users to login page
@user_passes_test(superuser_check, login_url='/accounts/login/')
def adminDashboard(request):
    # Fetch relevant data to populate admin dashboard fields and forms
    questions = quiz.objects.filter(locationID='0').values_list("question", flat=True)
    locations = QuizLocation.objects.values_list("locationName", flat=True)
    allLocations = QuizLocation.objects.all()
    bins = Bin.objects.values_list("binIdentifier", flat=True)
    blocks = Block.objects.all()
    users = CustomUser.objects.all()
    allBins = Bin.objects.all()

    # Handle various POST request actions for creating, editing, or deleting entities
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # Add a new quiz question for default location (locationID='0')
        if "question" in request.POST and "answer" in request.POST:
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

        # Delete an existing quiz question
        elif "question" in request.POST:
            question_to_delete = request.POST["question"]
            quiz.objects.filter(question=question_to_delete).delete()
            return redirect("admin-dashboard")

        # Edit existing location details
        elif form_type == "edit_location":
            location_id = request.POST.get("location_id")
            location = QuizLocation.objects.get(locationID=location_id)
            location.longitude = request.POST.get("longitude")
            location.latitude = request.POST.get("latitude")
            location.name = request.POST.get("location_name")
            location.save()
            return redirect("admin-dashboard")

        # Edit existing bin details (location and identifier update)
        if request.POST.get('form_type') == 'edit_bin':
            bin_id = request.POST.get('bin_id')
            bin_instance = Bin.objects.get(binID=bin_id)
            bin_instance.binIdentifier = request.POST.get('bin_identifier')
            bin_instance.latitude = request.POST.get('latitude')
            bin_instance.longitude = request.POST.get('longitude')
            bin_instance.save()
            return redirect('admin-dashboard')

        # Add a new quiz location along with its associated questions
        elif "longitude" in request.POST and "latitude" in request.POST and "location_name" in request.POST:
            new_location = QuizLocation(
                longitude=request.POST["longitude"],
                latitude=request.POST["latitude"],
                locationName=request.POST["location_name"],
            )
            new_location.save()

            # Add multiple questions associated with the newly created location
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

        # Delete quiz location and its associated questions
        elif "location_name" in request.POST:
            location_to_delete = request.POST["location_name"]
            locationID = QuizLocation.objects.get(locationName=location_to_delete).locationID
            quiz.objects.filter(locationID=locationID).delete()
            QuizLocation.objects.filter(locationName=location_to_delete).delete()
            return redirect("admin-dashboard")

        # Add new recycling bin data
        elif "longitude" in request.POST and "latitude" in request.POST and "bin_identifier" in request.POST:
            new_bin = Bin(
                longitude=request.POST["longitude"],
                latitude=request.POST["latitude"],
                binIdentifier=request.POST["bin_identifier"]
            )
            new_bin.save()
            return redirect("admin-dashboard")

        # Delete existing recycling bin
        elif "bin_identifier" in request.POST:
            bin_to_delete = request.POST["bin_identifier"]
            Bin.objects.filter(binIdentifier=bin_to_delete).delete()

        # Edit existing garden block details via provided form data
        if request.POST.get("form_type") == "edit_block":
            block = get_object_or_404(Block, blockID=request.POST.get("blockID"))
            form = EditBlockForm(request.POST, instance=block)
            if form.is_valid():
                form.save()
                return redirect("admin-dashboard")

        # Create a new garden block
        elif request.POST.get("form_type") == "add_block":
            form = BlockForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("admin-dashboard")

        # Update user information, specifically their role
        elif form_type == "edit_user":
            user_id = request.POST.get("user_id")
            user_obj = get_object_or_404(CustomUser, id=user_id)
            edit_form = EditUserForm(request.POST, instance=user_obj)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("admin-dashboard")

    # Initialize an empty BlockForm when the request method is GET (non-POST requests)
    else:
        form = BlockForm()

    # Reinitialize form regardless of POST or GET to ensure it's always available in the context
    form = BlockForm()

    # Render the admin dashboard HTML template with context data including forms and entities data
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
