# Author: Edward Pratt, Ethan Clapham
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Stats
from ..accounts.models import CustomUser

# Create your views here.

# View for the stats app /stats/
@login_required
def statspage(request):
    user = CustomUser.objects.get(id=request.user.id)
    stats, created = Stats.objects.get_or_create(userID=user)

    # Convert items to kg using estimated weight per item
    plastic_kg = stats.plasticRecycled * 0.02
    metal_kg = stats.metalRecycled * 0.05
    paper_kg = stats.paperRecycled * 0.015
    packaging_kg = stats.packagingRecycled * 0.03

    # Plastic saved formula (kg)
    plastic_saved_kg = plastic_kg * 0.8  # 80% of recycled plastic reduces new production

    # CO₂ saved formula (kg)
    co2_saved_kg = (
        plastic_kg * 1.5 +   # Plastic CO₂ savings
        metal_kg * 2.5 +     # Metal CO₂ savings
        paper_kg * 1.3 +     # Paper CO₂ savings
        packaging_kg * 1.1   # Packaging CO₂ savings
    )

    content = {
        'user_points' : stats.yourPoints,
        'plastic_saved' : plastic_saved_kg,
        'co2_saved' : co2_saved_kg,
    }

    return render(request, "statistics.html", content)
