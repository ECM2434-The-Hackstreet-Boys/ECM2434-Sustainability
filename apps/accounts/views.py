"""Author: Edward Pratt"""

from django import forms
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm

User = get_user_model()

class RoleUpdateForm(forms.ModelForm):
    """Form for updating the role of a User."""

    class Meta:
        """Meta class for updating the user role"""
        model = User
        fields = ['role']


# View for registering new users
def register(request):
    """
    Handle user registration.

    - Redirects authenticated users to the dashboard.
    - If the request method is POST, validates the registration form.
    - If valid, saves the new user, logs them in, and redirects to the dashboard.
    - If the request method is GET, renders the registration form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the registration page or redirects to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect logged-in users to the dashboard

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after registration
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# View for allowing registered users to log in
def user_login(request):
    """
    Handle user login.

    - Redirects authenticated users to the dashboard.
    - If the request method is POST, validates the login form.
    - If valid, logs the user in and redirects to the dashboard.
    - If invalid or if the request method is GET, renders the login form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the login page or redirects to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect logged-in users to the dashboard

    form = AuthenticationForm(data=request.POST) if request.method == "POST" else AuthenticationForm()

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after login

    return render(request, 'login.html', {'form': form})


def is_admin(user):
    """
    Check if a user has an admin role.

    Returns:
        bool: True if the user's role is "admin", otherwise False.
    """
    return bool(user.role == "admin")


# View for managing user roles (accessible only to admin users)
@login_required
def manage_roles(request):
    """
    Display and update user roles.

    - Restricts access to admin users.
    - Displays a list of all users and their roles.
    - Allows an admin to update a user's role via a form submission.
    - If a non-admin user attempts access, they are redirected with a warning message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the role management page or redirects unauthorized users.
    """
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
