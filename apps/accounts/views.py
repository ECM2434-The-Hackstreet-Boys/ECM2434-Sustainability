from django import forms
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm

User = get_user_model()

class RoleUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    form = AuthenticationForm(data=request.POST) if request.method == "POST" else AuthenticationForm()

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login.html', {'form': form})  # Always return a response




def is_admin(user):
    return bool(user.role == "admin")

@login_required

def manage_roles(request):
    if not is_admin(request.user):
        messages.warning(request, "You are not authorized to access this page.")
        return redirect("home")

    users = User.objects.all()
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        form = RoleUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect("manage_roles")  # Refresh the page

    else:
        form = RoleUpdateForm()

    return render(request, "manage_roles.html", {"users": users, "form": form})