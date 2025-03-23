from django.urls import path
from .views import update_settings, delete_account

urlpatterns = [
    path("", update_settings, name="settings"),
    path("delete-account/", delete_account, name="delete_account"),
]