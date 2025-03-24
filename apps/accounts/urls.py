"""Author: Edward Pratt"""

from django.urls import path
from .views import register, user_login, manage_roles
from django.contrib.auth.views import LogoutView


# URL patterns for the accounts app accounts/
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('manage_roles/', manage_roles, name='manage_roles'),
    path('logout/', LogoutView.as_view(), {"next_page": "home"}, name='logout'),
]