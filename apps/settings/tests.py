"""
Tests for the Settings page

Tests if users can modify their account status, change username or password,
and if the user has the ability to delete their account.

@version: 1.0
@date: 2025-03-21
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.

class SettingsPageTests(TestCase):
    """Test cases for accessing the settings page."""

    def setUp(self):
        """Create a user for authentication."""
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_authenticated_settings_access(self):
        """Test if an authenticated user can access the settings page."""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("settings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "settings.html")

    def test_unauthenticated_access_to_settings_redirect(self):
        """Test if unauthenticated users are redirected from the settings page."""
        response = self.client.get(reverse("settings"))
        self.assertRedirects(response, "/accounts/login/?next=" + reverse("settings"))


class SettingsTests(TestCase):
    """Test cases for updating user settings and deleting accounts."""

    def setUp(self):
        """Create a user for testing."""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_settings_successful(self):
        """Test updating username and password successfully."""
        response = self.client.post(reverse("settings"), {
            "username": "newusername",
            "password": "newpassword123"
        })
        self.assertRedirects(response, reverse("settings"))

        # Refresh the user instance
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")
        self.assertTrue(self.user.check_password("newpassword123"))

    def test_settings_no_changes(self):
        """Test submitting an empty form without changing username or password."""
        response = self.client.post(reverse("settings"), {})
        self.assertRedirects(response, reverse("settings"))

        # Ensure the username and password remain unchanged
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("password123"))

    def test_settings_partial_update(self):
        """Test updating only the username while keeping the existing password."""
        response = self.client.post(reverse("settings"), {
            "username": "partialupdate"
        })
        self.assertRedirects(response, reverse("settings"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "partialupdate")
        self.assertTrue(self.user.check_password("password123"))  # Password remains the same

    def test_update_settings_short_password(self):
        """Test updating the password with an invalid short password."""
        response = self.client.post(reverse("settings"), {
            "username": self.user.username,  # Keep the current username
            "password": "123"  # Too short
        })
        self.assertRedirects(response, reverse("settings"))

        # Check if the error message exists in Django messages
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("password" in str(message) for message in messages))  # Ensure error was raised

        # Ensure the password did NOT change
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password("123"))  # Password should remain unchanged
        self.assertEqual(self.user.username, "testuser")  # Username should remain unchanged

    def test_delete_account_successful(self):
        """Test deleting the user account successfully."""
        response = self.client.post(reverse("delete_account"))
        self.assertRedirects(response, reverse("home"))

        # Ensure the user is deleted
        user_exists = User.objects.filter(username="testuser").exists()
        self.assertFalse(user_exists)

    def test_delete_account_without_post(self):
        """Test accessing delete_account via GET should not delete the account."""
        response = self.client.get(reverse("delete_account"))
        self.assertEqual(response.status_code, 200)

        # Ensure the user still exists
        user_exists = User.objects.filter(username="testuser").exists()
        self.assertTrue(user_exists)

    def test_unauthenticated_access_to_settings_post(self):
        """Ensure unauthenticated users cannot update settings."""
        self.client.logout()
        response = self.client.post(reverse("settings"), {
            "username": "hacker",
            "password": "newpassword"
        })
        self.assertRedirects(response, "/accounts/login/?next=" + reverse("settings"))

    def test_unauthenticated_access_to_delete_account(self):
        """Ensure unauthenticated users cannot delete an account."""
        self.client.logout()
        response = self.client.post(reverse("delete_account"))
        self.assertRedirects(response, "/accounts/login/?next=" + reverse("delete_account"))
