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

    content = {
        'user_points' : stats.yourPoints,
        'packaging_recycled' : stats.packagingRecycled,
        'plastic_recycled' : stats.plasticRecycled,
        'metal_recycled' : stats.metalRecycled,
        'paper_recycled' : stats.paperRecycled,
    }

    return render(request, "statistics.html", content)
