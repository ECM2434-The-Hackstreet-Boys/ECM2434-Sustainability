# Author: Ethan Clapham
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..stats.models import Stats
from ..accounts.models import CustomUser

# Create your views here.


# View to access the recycling page
@login_required
def recyclepage(request):

    return render(request, "recycling.html")

def submit_recycling(request):
    if request.method == "POST":
        user = CustomUser.objects.get(id=request.user.id)

        stats, created = Stats.objects.get_or_create(userID=user)

        stats.packagingRecycled += int(request.POST.get("food-packaging", 0))
        stats.plasticRecycled += int(request.POST.get("plastic", 0))
        stats.metalRecycled += int(request.POST.get("metal", 0))
        stats.paperRecycled += int(request.POST.get("paper", 0))
        stats.save()

        return(redirect("dashboard"))
    
    return render(request, "recycling.html")