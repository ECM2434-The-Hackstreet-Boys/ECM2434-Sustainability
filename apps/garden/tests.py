from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.

class GardenPageTests(TestCase):
    def setUp(self):
        # Create a user to test logged-in behaviour
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_garden_page_logged_in(self):
        # Test if the garden page is accessible when logged in
        self.client.login(username='testuser', password='testpassword#123') # Log in with the created user
        response = self.client.get(reverse('garden')) # Make a GET request to the garden page
        self.assertEqual(response.status_code, 200) # Check if the status code is 200 (OK)
        self.assertTemplateUsed(response, 'garden.html') # Check if the correct template is used

    def test_garden_page_logged_out(self):
        # Test if the garden page is inaccessible when logged out
        response = self.client.get(reverse('garden'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('garden')) # Check if the user is redirected to the login page

class GardenLoadTests(TestCase):
    def setUp(self):
        # Create a user to test logged-in behaviour
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_load_garden_logged_in(self):
        # Test if the load garden endpoint is accessible when logged in
        self.client.login(username='testuser', password='testpassword#123') # Log in with the created user
        response = self.client.get(reverse('load_garden')) # Make a GET request to the load garden endpoint
        self.assertEqual(response.status_code, 200) # Check if the status code is 200 (OK)

    def test_load_garden_logged_out(self):
        # Test if the load garden endpoint is inaccessible when logged out
        response = self.client.get(reverse('load_garden'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('load_garden')) # Check if the user is redirected to the login page

class GardenSaveTests(TestCase):
    def setUp(self):
        # Create a user to test logged-in behaviour
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_save_garden_logged_in(self):
        # Test if the save garden endpoint is accessible when logged in
        self.client.login(username='testuser', password='testpassword#123') # Log in with the created user
        response = self.client.post(reverse('save_garden')) # Make a POST request to the save garden endpoint
        self.assertEqual(response.status_code, 200) # Check if the status code is 200 (OK)

    def test_save_garden_logged_out(self):
        # Test if the save garden endpoint is inaccessible when logged out
        response = self.client.post(reverse('save_garden'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('save_garden')) # Check if the user is redirected to the login page
