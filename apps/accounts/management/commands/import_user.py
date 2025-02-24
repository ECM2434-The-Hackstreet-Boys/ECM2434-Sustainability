# Author: Edward Pratt
# Last Modified: 2025-02-23

from django.core.management.base import BaseCommand
from apps.accounts.models import CustomUser


class Command(BaseCommand):
    help = "Setup test accounts for user and admin"

    def handle(self, *args, **kwargs):
        # Create or get user account

        # Attempts to create a new user account with the username "user" and email "user:@user.com" with the role
        # "user". If the user account is created successfully, the password is set to "user" and the user account is
        # saved. A success message is displayed in the console. If the user account already exists, a warning message
        # is displayed in the console.
        user, created = CustomUser.objects.get_or_create(
            username="user",
            defaults={
                "email": "user@user.com",
                "role": "user"
            }
        )
        # If the user account is created successfully, the password is set to "user" and the user account is saved.
        if created:
            user.set_password("user")
            user.save()
            self.stdout.write(self.style.SUCCESS("User account created."))
        else:
            self.stdout.write(self.style.WARNING("User account already exists."))


        # Attempts to create a new admin account with the username "admin" and email "admin:@admin.com" with the role admin
        admin, created = CustomUser.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@admin.com",
                "role": "admin"
            }
        )
        # If the admin account is created successfully, the password is set to "admin" and the user account is saved.
        if created:
            admin.set_password("admin")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Admin account created."))
        else:
            self.stdout.write(self.style.WARNING("Admin account already exists."))
