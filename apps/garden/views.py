# @Author:  Edward Pratt

import json
import os

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from SustainabilityApp import settings
from .models import Garden

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

# View for loading the garden page
@login_required
def get_garden_page(request):
    return render(request, 'garden.html')


def is_admin(user):
    return bool(user.role == "admin")


# View for loading the admin garden page
@login_required
def get_admin_page(request):
    if not is_admin(request.user):
        messages.warning(request, "You are not authorized to access this page.")
        return redirect("home")

    else:
        return render(request, 'admin_garden.html')

# View for loading the garden data and sending it to the webpage
@login_required
def load_garden(request):
    try:
        user = request.user  # Ensure user is authenticated
        garden = get_object_or_404(Garden, userID=user)

        file_path = os.path.join(settings.MEDIA_ROOT, str(garden.file_path))

        if not os.path.exists(file_path):
            return JsonResponse({"success": False, "error": "Garden file not found!"}, status=404)

        with open(file_path, "r") as f:
            tile_data = json.load(f)

        return JsonResponse({"success": True, "garden": tile_data})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


# View for saving the garden to a file and adding it to the database
@csrf_exempt
@login_required
def save_garden(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            garden_name = data.get("name", "default_garden")
            tile_data = data.get("garden", {})

            user = request.user  # Ensure user is authenticated

            # Define file path
            file_path = os.path.join(settings.MEDIA_ROOT, "gardens", f"{user.username}_{garden_name}.json")
            if not os.path.exists(file_path):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save JSON to file
            with open(file_path, "w") as f:
                print(tile_data)
                json.dump(tile_data, f)

            # Save file path in database
            Garden.objects.update_or_create(
                userID=user,
                defaults={"file_path": f"gardens/{user.username}_{garden_name}.json"}
            )

            return JsonResponse({"success": True, "message": "Garden saved!"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)


