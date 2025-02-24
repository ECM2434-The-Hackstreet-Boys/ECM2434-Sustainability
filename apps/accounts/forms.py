# Author: Edward Pratt
# Last Modified: 2025-02-11

"""
This file contains the form for user registration.
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

"""Create a form for user registration"""
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # No role field
