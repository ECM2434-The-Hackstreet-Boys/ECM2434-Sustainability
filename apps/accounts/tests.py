"""Tests for the accounts app.

Tests to check if user registration, login, logout, and role management are 
working as expected.

@version: 1.0
@date: 2025-03-07
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class UserRegistrationTests(TestCase):
    """Tests user registration functionality."""
    def test_valid_user_registration(self):
        """Test if user registration is successful with valid data."""
        # Create a user
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword#123',
            'password2': 'testpassword#123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists()) # Check if user exists

    def test_invalid_user_registration(self):
        """Tests if user registration is unsuccessfuly with invalid data"""
        # Create a user with invalid data
        response = self.client.post(reverse('register'), {
            'username': '',
            'email': 'invalidemail',
            'password1': 'pass123',
            'password2': 'pass4567'
        })
        self.assertEqual(response.status_code, 200) # Should return 200 as the form is invalid
        self.assertFalse(User.objects.filter(email='invalidemail').exists())
        self.assertContains(response, "This field is required.") # Check for error message
        self.assertContains(response, "Enter a valid email address.") # Check for error message
        self.assertContains(response, "The two password fields didn’t match.") # Check for error message

    def test_duplicate_user_registration(self):
        """Tests if duplicate user registration fails."""
        User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword#123")

        response = self.client.post(reverse('register'), {
            'username': 'testuser',  # Duplicate username
            'email': 'testuser@example.com',  # Duplicate email
            'password1': 'testpassword#123',
            'password2': 'testpassword#123',
        })

        self.assertEqual(response.status_code, 200)  # Form should return validation error
        self.assertContains(response, "A user with that username already exists.")

class UserLoginTests(TestCase):
    """Tests user login functionality."""

    # Login with valid credentials
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123') # Create a user

    def test_valid_user_login(self):
        """Tests if the user can login with valid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword#123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, reverse('dashboard'))

    def test_invalid_user_login(self):
        """Tests if the user cannot login with invalid credentials."""
        # Login with invalid credentials
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password. Note that both fields may be case-sensitive.") # Check for error message

    def test_blank_user_login(self):
        """Tests if login with blank username or password fails."""
        response = self.client.post(reverse('login'), {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        # The result cannot be printed, due to the error message being built-in to Django's HTML file

    def test_case_sensitive_username_login(self):
        """Tests if login fails due to case sensitivity in the username."""
        response = self.client.post(reverse('login'), {
            'username': 'TESTUSER',  # Wrong case
            'password': 'testpassword#123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")

class UserLogoutTest(TestCase):
    """Tests user logout functionality."""
    def setUp(self):
        """Sets up a user for testing."""
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_user_logout(self):
        """Tests if the user can logout."""
        # Test if user can logout
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.post(reverse('logout'))  # Use POST instead of GET
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))  # Check for redirection

    def test_logout_without_login(self):
        """Tests if logging out without an active session still redirects to home."""
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
