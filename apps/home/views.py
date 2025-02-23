from django.shortcuts import render

# Create your views here.

# Homepage view
def homepage(request):
    return render(request, "home.html")