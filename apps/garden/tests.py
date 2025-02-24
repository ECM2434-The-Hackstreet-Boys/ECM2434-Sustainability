"""Tests for the garden apps.

    Tests if the garden page is accessible when logged in, if the garden can save correctly, and if the garden load
    can load correctly from an existing save file.

    @version: 1.0
    @author: Sandy Hay
"""

import os
import json
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Garden

User = get_user_model()

# Create your tests here.

class GardenPageTests(TestCase):
    """Tests if the garden page can be accessed."""
    def setUp(self):
        """Sets up a user for testing the garden access."""
        # Create a user to test logged-in behaviour
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_garden_page_logged_in(self):
        """Tests if a logged in user can access the garden page."""
        # Test if the garden page is accessible when logged in
        self.client.login(username='testuser', password='testpassword#123') # Log in with the created user
        response = self.client.get(reverse('garden')) # Make a GET request to the garden page
        self.assertEqual(response.status_code, 200) # Check if the status code is 200 (OK)
        self.assertTemplateUsed(response, 'garden.html') # Check if the correct template is used

    def test_garden_page_logged_out(self):
        """Tests if a logged out user cannot access the garden page."""
        # Test if the garden page is inaccessible when logged out
        response = self.client.get(reverse('garden'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('garden')) # Check if the user is redirected to the login page

class SaveGardenTest(TestCase):
    """Tests if the garden saved safely and correctly"""
    def setUp(self):
        """Set ups a test garden from a logged in user to saves to a set file path
        
            - Sets up a test user
            - Sets up a client
            - Logs the user into the website
            - Creates a name for the garden for the test user
            - Sets up the file path location for the garden to be saved and stored in
        """
        # Create a user to test saving functionality
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword#123')

        self.garden_name = "my_test_garden"
        self.file_path = os.path.join(settings.MEDIA_ROOT, 'gardens', f"{self.user.username}_{self.garden_name}.json")

    def test_save_garden_logged_in(self):
        """Test if the garden is saved correctly when the user is logged in."""
        garden_data = {
            "name": self.garden_name,
            "garden": {
                "tiles": [
                    {"x": 0, "y": 0, "type": "grass"},
                    {"x": 1, "y": 0, "type": "grass"},
                    {"x": 0, "y": 1, "type": "water"},
                    {"x": 1, "y": 1, "type": "water"}
                ]
            }
        }

        response = self.client.post(
            reverse('save_garden'),
            json.dumps(garden_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertTrue(response_data.get("success"))
        self.assertEqual(response_data.get("message"), "Garden saved!")

        # Verify the garden file is created
        self.assertTrue(os.path.exists(self.file_path))

        # Verify the database entry is updated
        garden = Garden.objects.get(userID=self.user)
        self.assertEqual(garden.file_path, f"gardens/{self.user.username}_{self.garden_name}.json")

    def test_save_garden_file_creation(self):
        """Ensure the garden file is actually saved in the correct directory."""
        garden_data = {'name': self.garden_name, "garden": {"tiles": [{'x': 2, 'y': 2, "type": "grass"}]}}

        self.client.post(reverse("save_garden"), json.dumps(garden_data), content_type="application/json")

        # Check if file exists
        self.assertTrue(os.path.exists(self.file_path))

        # Check file content
        with open(self.file_path, 'r') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, garden_data["garden"])

    def test_save_garden_unauthenticated(self):
        """Test that an unauthenticated user cannot save a garden."""
        self.client.logout()

        garden_data = {"name": self.garden_name, "garden": {"tiles": [{'x': 3, 'y' : 3, "type": "tree"}]}}

        response = self.client.post(reverse("save_garden"), json.dumps(garden_data), content_type="application/json")
        
        # Expecting a 302 (Redirect to login) status code
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        """Clean up created test files."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

class LoadGardenTests(TestCase):
    """Tests if the garden can be loaded from an existing garden save from a test user"""
    def setUp(self):
        """Sets up a save garden file, ready to be loaded in from a test user

            (Same steps for the save garden tests set-up except)
            - Creates the test garden ready to be saved
            - Makes a directory for the test garden
            - Adds data to the test garden
            - Saves the garden to the directory
        """
        # Create a user to test loading functionality
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword#123')

        # Create a test garden
        self.garden_name = "my_test_garden"
        # Set the file path for the test garden
        self.file_path = os.path.join(settings.MEDIA_ROOT, "gardens", f"{self.user.username}_{self.garden_name}.json")

        self.garden = Garden.objects.create(userID=self.user, file_path=f"gardens/{self.user.username}_{self.garden_name}.json")

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.test_garden_data = {"name": self.garden_name, "garden": {"tiles": [{'x': 0, 'y': 0, "type": "grass"}, {'x': 1, 'y' : 1, "type": "tree"}]}}

        with open(self.file_path, 'w') as f:
            json.dump(self.test_garden_data, f)

    def test_load_garden_success(self):
        """Test if an authenticated user can successfullly load their garden."""
        response = self.client.get(reverse("load_garden")) # Ensure this matches

        # Expecting a 200 (OK) status code
        self.assertEqual(response.status_code, 200)

        # Verify response JSON
        response_data = response.json()
        self.assertTrue(response_data.get("success"))
        self.assertEqual(response_data.get("garden"), self.test_garden_data)

    def test_load_garden_file_not_found(self):
        """Test if the garden file is not found/does not exist."""
        os.remove(self.file_path) # Delete the file to simulate missing file scenario

        response = self.client.get(reverse("load_garden"))

        # Expecting a 404 (Not Found) status code
        self.assertEqual(response.status_code, 404)

        # Check erro message
        response_data = response.json()
        self.assertFalse(response_data.get("success"))
        self.assertEqual(response_data.get("error"), "Garden file not found!")

    def test_load_garden_unauthenticated(self):
        """Test that an unauthenticated user cannot load a garden."""
        self.client.logout()

        response = self.client.get(reverse("load_garden"))

        # Expecting a 302 (Redirect to login) status code
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        """Clean up created test files."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        self.garden.delete()