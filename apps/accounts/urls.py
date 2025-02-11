from django.urls import path
from .views import register, user_login, manage_roles

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('manage_roles/', manage_roles, name='manage_roles'),
]