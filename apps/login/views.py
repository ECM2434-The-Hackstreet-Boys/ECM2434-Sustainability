from django.shortcuts import render

# Create your views here.
def loginpage(request):

    return render(request, "home.html")