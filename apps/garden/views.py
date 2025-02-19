import json
import os

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from SustainabilityApp import settings
from .models import Garden


# Create your views here.

def get_garden_page(request):
    return render(request, 'garden.html')


def get_admin_page(request):
    return render(request, 'admin_garden.html')


def load_garden(request, name):
    try:
        user = request.user  # Ensure user is authenticated
        garden = get_object_or_404(Garden, user=user, name=name)

        file_path = os.path.join(settings.MEDIA_ROOT, str(garden.file_path))

        if not os.path.exists(file_path):
            return JsonResponse({"success": False, "error": "Garden file not found!"}, status=404)

        with open(file_path, "r") as f:
            tile_data = json.load(f)

        return JsonResponse({"success": True, "tiles": tile_data})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@csrf_exempt
def save_garden(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            garden_name = data.get("name", "default_garden")
            tile_data = data.get("tiles", {})

            user = request.user  # Ensure user is authenticated

            # Define file path
            file_path = os.path.join(settings.MEDIA_ROOT, "gardens", f"{user.username}_{garden_name}.json")

            # Save JSON to file
            with open(file_path, "w") as f:
                json.dump(tile_data, f)

            # Save file path in database
            garden, created = Garden.objects.update_or_create(
                user=user,
                name=garden_name,
                defaults={"file_path": f"gardens/{user.username}_{garden_name}.json"}
            )

            return JsonResponse({"success": True, "message": "Garden saved!"})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)