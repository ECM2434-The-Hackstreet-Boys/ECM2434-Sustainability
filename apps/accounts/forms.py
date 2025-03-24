# Author: Edward Pratt
# Last Modified: 2025-02-11

"""
This file contains the form for user registration.
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django.forms import ModelForm

from .models import CustomUser

User = get_user_model()

class RegisterForm(UserCreationForm):
    """Create a form for user registration"""
    class Meta:
        """Meta class for inputting user credentials"""
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # No role field


class EditUserForm(ModelForm):
    """Form for editing only the user's role."""
    class Meta:
        """Meta class for editing the user's role"""
        model = CustomUser
        fields = ['role']
