"""

"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class UserRegistrationTests(TestCase):
    def test_valid_user_registration(self):
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

class UserLoginTests(TestCase):
    def test_valid_user_login(self):
        # Login with valid credentials
        def setUp(self):
            self.user = User.objects.create_user(username='testuser', password='testpassword#123') # Create a user

        def test_valid_user_login(self):
            response = self.client.post(reverse('login'), {
                'username': 'testuser',
                'password': 'testpassword#123'
            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url, reverse('dashboard'))

    def test_invalid_user_login(self):
        # Login with invalid credentials
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password. Note that both fields may be case-sensitive.") # Check for error message

class AuthenticatedUserAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123') 

    def test_valid_dashboard_access_test(self):
        # Test if user can access dashboard
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to your dashboard") # Check for dashboard content

    def test_invalid_dashboard_access_test(self):
        # Test if user can access dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302) # Redirect to login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('dashboard')) # Check for redirection

class UserLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_user_logout(self):
        # Test if user can logout
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.post(reverse('logout'))  # Use POST instead of GET
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))  # Check for redirection

class UserRolesTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', role='admin')
        self.normal_user = User.objects.create_user(username='user', password='userpass', role='user')

    def test_admin_manage_roles(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('manage_roles')) # Try to access manage roles page
        self.assertEqual(response.status_code, 200) # Should return 200

    def test_non_admin_manage_roles(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('manage_roles'))
        self.assertEqual(response.status_code, 302) # Redirect to login page
        self.assertRedirects(response, reverse('home')) # Check for redirection

    # def test_admin_updates_user_role(self):
    #     self.client.login(username='admin', password='adminpass')
    #     response = self.client.post(reverse('manage_roles'), {
    #         'user': self.normal_user.id,
    #         'role': 'admin' # Change role to admin
    #     })
    #     self.normal_user.refresh_from_db() # Reload user from database
    #     self.assertEqual(self.normal_user.role, 'admin') # Role should be updated
    #     self.assertEqual(response.status_code, 302) # Should redirect after successful update

    # def test_admin_deletes_user(self):
    #     self.client.login(username='admin', password='adminpass')

    # def test_gamekeeper_adds_ecostop(self):
    #     self.client.login(username='gamekeeper', password='gamekeeperpass')