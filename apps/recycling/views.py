# Author: Ethan Clapham
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..stats.models import Stats
from ..accounts.models import CustomUser
from .models import Bin

# Create your views here.


# View to access the recycling page
@login_required
def recyclepage(request, bin_id):
    # Fetch bin details
    bin_obj = get_object_or_404(Bin, binID=bin_id)

    # Pass bin coordinates to the template
    context = {
        'bin_id' : bin_id,
        'bin_lat' : bin_obj.latitude,
        'bin_long' : bin_obj.longitude,
    }

    return render(request, "recycling.html", context)

# View to submit recycling data
@login_required
def submit_recycling(request):
    if request.method == "POST":
        user = CustomUser.objects.get(id=request.user.id)

        stats, created = Stats.objects.get_or_create(userID=user)

        def safe_int(value):
            try:
                # Convert to int and check if it's non-negative
                result = int(value)
                return result if result >= 0 else 0  # Ensure negative values return 0
            except ValueError:
                return 0  # Ignore invalid input

        stats.packagingRecycled += safe_int(request.POST.get("food-packaging", 0))
        stats.plasticRecycled += safe_int(request.POST.get("plastic", 0))
        stats.metalRecycled += safe_int(request.POST.get("metal", 0))
        stats.paperRecycled += safe_int(request.POST.get("paper", 0))
        stats.save()

        return redirect("dashboard")

    return render(request, "recycling.html")
