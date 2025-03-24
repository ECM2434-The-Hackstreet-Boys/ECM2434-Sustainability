# @Author:  Edward Pratt

import json
import os

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from SustainabilityApp import settings
from apps.stats.models import Stats
from .models import Garden, Block, Inventory

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
    if not is_admin(request.user): # Ensure user is an admin
        messages.warning(request, "You are not authorized to access this page.")
        return redirect("home")

    else: # Load the admin garden page
        return render(request, 'admin_garden.html')

# View for loading the garden data and sending it to the webpage
@login_required
def load_garden(request):
    try:
        user = request.user  # Ensure user is authenticated
        garden = get_object_or_404(Garden, userID=user)

        # Set file path to garden
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
            data = json.loads(request.body) # Loads the JSON data from the request
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


@login_required
def asset_list(request):
    assets = list(Block.objects.values("name", 'blockPath'))
    return JsonResponse({"assets": assets})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Inventory, Block

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Inventory, Block

@csrf_exempt
@login_required
def place_block(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        block_name = data.get("blockName")
        removed_block_name = data.get("currentTile")  # Block being swapped out

        # Ensure the block being placed exists
        block = Block.objects.filter(name=block_name).first()
        if not block:
            return JsonResponse({"success": False, "message": f"Block '{block_name}' does not exist!"}, status=400)

        # Ensure the block being removed exists
        removed_block = Block.objects.filter(name=removed_block_name).first()

        # Get or create the inventory entry for the placed block
        inventory, created = Inventory.objects.get_or_create(userID=user, blockID=block)

        if inventory.quantity > 0:
            inventory.quantity -= 1
            inventory.save()

            # Add back the removed block (if valid)
            if removed_block:
                add_block_to_inventory(user, removed_block)

            return JsonResponse({"success": True, "message": "Block placed!"}, status=200)
        else:
            return JsonResponse({"success": False, "message": "Not enough blocks in inventory!"}, status=200)

    return JsonResponse({"success": False, "message": "Invalid request!"}, status=400)


def add_block_to_inventory(user, block):
    """
    Adds a block to the user's inventory if it exists.
    If the block is not in the inventory, it is added with quantity 1.
    """
    inventory, created = Inventory.objects.get_or_create(userID=user, blockID=block)

    if not created:
        inventory.quantity += 1
        inventory.save()


@csrf_exempt
@login_required
def remove_block_from_inventory(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user
        block_name = data.get("currentTile")

        try:
            block = Block.objects.get(name=block_name)
            add_block_to_inventory(user, block)  # Now correctly adds block if not in inventory
            return JsonResponse({"success": True, "message": "Block removed and added to inventory!"}, status=200)
        except Block.DoesNotExist:
            return JsonResponse({"success": False, "message": "Block does not exist!"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request!"}, status=400)

@login_required
def get_store_items(request):
    user_inventory = {item["blockID"]: item["quantity"] for item in Inventory.objects.filter(userID=request.user).values("blockID", "quantity")}
    user_stats = Stats.objects.get_or_create(userID=request.user)
    user_points = user_stats[0].yourPoints

    items = list(Block.objects.values("blockID", "name", "visibleName", "blockPath", "cost", "value"))

    for item in items:
        item["owned"] = user_inventory.get(item["blockID"], 0)  # Get owned count or default to 0

    return JsonResponse({"items": items, "points": user_points})

@login_required
def buy_item(request):
    if request.method == "POST":
        data = json.loads(request.body)
        item_id = data.get("itemId")
        user = request.user
        cost = data.get("cost")
        quantity = data.get("quantity")

        if not item_id or cost is None or quantity is None:
            return JsonResponse({"success": False, "message": "Invalid data"})

        try:
            block = Block.objects.get(blockID=item_id)
            userStats = Stats.objects.get(userID=user)
        except Block.DoesNotExist:
            return JsonResponse({"success": False, "message": "Block not found"}, status=404)

        total_cost = cost

        if userStats.yourPoints < total_cost:
            return JsonResponse({"success": False, "message": "Insufficient funds"}, status=404)

        userStats.yourPoints -= total_cost
        userStats.save()

        inventory, created = Inventory.objects.get_or_create(userID=user, blockID=block)
        inventory.quantity += quantity
        inventory.save()

        return JsonResponse({"success": True, "message": "Item(s) purchased!"})

    return JsonResponse({"success": False, "message": "Invalid request!"}, status=400)
