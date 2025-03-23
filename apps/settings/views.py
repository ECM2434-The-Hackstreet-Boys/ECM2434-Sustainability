from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model

# Create your views here.

def settings(request):
    return render(request, 'settings.html')

@login_required
def update_settings(request):
    if request.method == "POST":
        new_username = request.POST.get("username")
        new_password = request.POST.get("password")

        user = request.user
        if new_username:
            user.username = new_username
        
        if new_password:
            try:
                validate_password(new_password, user)
                user.set_password(new_password)
            except ValidationError as e:
                messages.error(request, " ".join(e.messages))
                return redirect("settings")

        user.save()
        update_session_auth_hash(request, user)  # Prevent logout
        messages.success(request, "Your settings have been updated successfully!")
        return redirect("settings")

    return render(request, "settings.html")

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("home")  # Redirect to home or login page

    return render(request, "settings.html")