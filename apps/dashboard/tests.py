"""Tests for the dashboard page

Tests to see if the user gets redirected to the dashboard

@version: 1.0
@date: 2025-03-07
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.

class AuthenticatedUserDashboardTests(TestCase):
    """Tests related to user authentication and dashboard access"""

    def setUp(self):
        """Sets up a user for testing"""
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_valid_dashboard_access_test(self):
        """Tests if an authenticated user can access the dashboard"""
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to your dashboard")

    def test_invalid_dashboard_access_test(self):
        """Tests if an unauthenticated user is redirected to the login page when accessing the dashboard"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('dashboard'))

    def test_authenticated_user_redirected_from_login(self):
        """Tests that an already logged-in user is redirected from the login page to the dashboard"""
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_authenticated_user_redirected_from_register(self):
        """Tests that an already logged-in user is redirected from the register page to the dashboard"""
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_successful_login_redirects_to_dashboard(self):
        """Tests if a user is redirected to the dashboard after login"""
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword#123'})
        self.assertEqual(response.status_code, 302)  # Expecting redirect
        self.assertRedirects(response, reverse('dashboard'))

    def test_successful_registration_redirects_to_dashboard(self):
        """Tests if a new user is redirected to the dashboard after registration"""
        response = self.client.post(reverse('register'), {
            'username': 'testuser2',
            'email'   : 'testuser2@example.com',
            'password1': 'testpassword#234',
            'password2': 'testpassword#234',
        })
        self.assertEqual(response.status_code, 302)  # Expecting redirect
        self.assertRedirects(response, reverse('dashboard'))
