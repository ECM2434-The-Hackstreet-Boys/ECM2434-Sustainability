"""Tests for the admin page

@author: Edward Pratt
"""

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from apps.quiz.models import quiz
from apps.play_screen.models import QuizLocation
from apps.recycling.models import Bin
from apps.garden.models import Block

User = get_user_model()


class AccessControlTests(TestCase):
    def setUp(self):
        """
        Set up test users with different roles for access control tests.
        """
        # Create a normal user without special permissions
        self.normal_user = User.objects.create_user(username='normal_user', password='password')
        # Create a user with 'gamekeeper' role
        self.gamekeeper_user = User.objects.create_user(username='gamekeeper_user', password='password',
                                                        role='gamekeeper')
        # Create a user with 'admin' role
        self.admin_user = User.objects.create_user(username='admin_user', password='password', role='admin')

    def test_normal_user_redirected(self):
        """
        Test that a normal user is redirected to the login page
        when attempting to access the admin dashboard.
        """
        self.client.login(username='normal_user', password='password')
        response = self.client.get('/admin-dashboard/')
        self.assertRedirects(response, '/accounts/login/?next=/admin-dashboard/', fetch_redirect_response=False)

    def test_gamekeeper_user_access(self):
        """
        Test that a user with the 'gamekeeper' role can access the admin dashboard.
        """
        self.client.login(username='gamekeeper_user', password='password')
        response = self.client.get('/admin-dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_admin_user_access(self):
        """
        Test that a user with the 'admin' role can access the admin dashboard.
        """
        self.client.login(username='admin_user', password='password')
        response = self.client.get('/admin-dashboard/')
        self.assertEqual(response.status_code, 200)


class AdminDashboardTests(TestCase):
    """
    Test suite for verifying the functionality of the admin dashboard.
    """

    def setUp(self):
        """
        Set up an admin user and log in to the test client for accessing the admin dashboard.
        """
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username='admin', password='pass123', role='admin'
        )
        # Create a test client and log in as the admin user
        self.client = Client()
        self.client.login(username='admin', password='pass123')

    def test_get_admin_dashboard(self):
        """
        Test that accessing the admin dashboard returns a 200 status code,
        uses the correct template, and contains the expected context data.
        """
        # Use reverse to resolve the URL name for the admin dashboard
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin.html')
        # Verify that context contains expected keys (e.g., 'questions', 'locations')
        self.assertIn('questions', response.context)
        self.assertIn('locations', response.context)


class QuizQuestionsTests(TestCase):
    """
    Test suite for managing quiz questions via the admin dashboard.
    """

    def setUp(self):
        """
        Set up the test environment by creating an admin user 
        and logging in with the test client.
        """
        self.admin_user = User.objects.create_user(
            username='admin', password='pass123', role='admin', is_superuser=True, is_staff=True,
        )
        # Create a test client and log in as the admin user
        self.client = Client()
        self.client.login(username='admin', password='pass123')

    def test_add_quiz_question(self):
        """
        Test that a new quiz question can be added successfully
        via a POST request to the admin dashboard.
        """
        question_text = "What is the capital of France?"
        # Assert that the question does not already exist
        self.assertFalse(quiz.objects.filter(question=question_text).exists())

        response = self.client.post(
            reverse('admin-dashboard'),
            {
                'question': question_text,
                'answer': "Paris",
                'incorrect1': "London",
                'incorrect2': "Berlin",
                'incorrect3': "Madrid"
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(quiz.objects.filter(question=question_text).exists())

    def test_delete_quiz_question(self):
        """
        Test deleting an existing quiz question via a POST request
        to the admin dashboard.
        """
        # First, create a test question
        test_question = quiz.objects.create(
            question="To be deleted",
            answer="Answer",
            other1="Inc1",
            other2="Inc2",
            other3="Inc3",
            locationID='0'
        )
        # Submit POST request to delete the question
        response = self.client.post(
            reverse('admin-dashboard'),
            {'question': test_question.question},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(quiz.objects.filter(question=test_question.question).exists())


class EditQuizLocationTests(TestCase):
    """
    Test suite for managing quiz locations via the admin dashboard.
    """

    def setUp(self):
        """
        Set up an admin user and log in to the test client
        for accessing the admin dashboard.
        """
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpassword',
            is_superuser=True,
            is_staff=True
        )
        self.client = Client()
        self.client.login(username='adminuser', password='adminpassword')

    def test_add_quiz_location(self):
        """
        Test that a new quiz location can be added successfully
        via a POST request to the admin dashboard.
        """
        location_name = "Test Location"
        longitude = 45.1234
        latitude = -94.5678
        # Assert that the location does not already exist
        self.assertFalse(QuizLocation.objects.filter(locationName=location_name).exists())

        response = self.client.post(
            reverse('admin-dashboard'),
            {
                'location_name': location_name,
                'longitude': longitude,
                'latitude': latitude,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(QuizLocation.objects.filter(locationName=location_name).exists())

    def test_edit_quiz_location(self):
        """
        Test editing an existing quiz location via a POST request 
        to the admin dashboard.
        """
        # Create an initial location
        location = QuizLocation.objects.create(
            longitude=12.3456,
            latitude=65.4321,
            locationName="Original Location"
        )

        # Edit the location
        response = self.client.post(
            reverse('admin-dashboard'),
            {
                'form_type': 'edit_location',
                'location_id': location.locationID,
                'longitude': 98.7654,
                'latitude': 12.3456,
                'location_name': "Updated Location"
            },
            follow=True
        )

        # Ensure the response is successful
        self.assertEqual(response.status_code, 200)

        # Refresh the location and verify the updates
        location.refresh_from_db()
        self.assertEqual(location.longitude, 98.7654)
        self.assertEqual(location.latitude, 12.3456)
        self.assertEqual(location.locationName, "Updated Location")

    def test_delete_quiz_location(self):
        """
        Test deleting an existing quiz location using a POST request 
        to the admin dashboard.
        """
        # Create a location to delete
        location = QuizLocation.objects.create(
            longitude=45.6789,
            latitude=23.4567,
            locationName="Location to Delete"
        )

        # Ensure the location exists
        self.assertTrue(QuizLocation.objects.filter(locationName="Location to Delete").exists())

        # Delete the location
        response = self.client.post(
            reverse('admin-dashboard'),
            {
                'location_name': "Location to Delete"
            },
            follow=True
        )

        # Ensure the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertFalse(QuizLocation.objects.filter(locationName="Location to Delete").exists())


class RecyclingBinTests(TestCase):
    """
    Test suite for managing recycling bins via the admin dashboard.
    """

    def setUp(self):
        """
        Set up an admin user and log in to the test client for accessing the admin dashboard.
        """
        admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpassword',
            is_superuser=True,
            is_staff=True
        )
        self.client.login(username='adminuser', password='adminpassword')

    def test_add_new_bin(self):
        """
        Test that a new recycling bin can be added successfully 
        via a POST request to the admin dashboard.
        """
        bin_identifier = "BIN123"
        # Assert that the bin does not already exist
        self.assertFalse(Bin.objects.filter(binIdentifier=bin_identifier).exists())

        response = self.client.post(
            reverse('admin-dashboard'),
            {
                'longitude': 10.1234,
                'latitude': 20.5678,
                'bin_identifier': bin_identifier
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Bin.objects.filter(binIdentifier=bin_identifier).exists())

    def test_edit_bin(self):
        """
        Test that an existing recycling bin's information can be updated
        via a POST request to the admin dashboard.
        """
        # Create a test bin
        test_bin = Bin.objects.create(
            binIdentifier="BIN123",
            longitude=10.1234,
            latitude=20.5678
        )

        # Edit the bin
        response = self.client.post(
            reverse('admin-dashboard'),
            {
                'form_type': 'edit_bin',
                'bin_id': test_bin.binID,
                'bin_identifier': "BIN456",
                'longitude': 30.1234,
                'latitude': 40.5678
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Fetch the edited bin
        test_bin.refresh_from_db()
        self.assertEqual(test_bin.binIdentifier, "BIN456")
        self.assertEqual(test_bin.longitude, 30.1234)
        self.assertEqual(test_bin.latitude, 40.5678)

    def test_delete_bin(self):
        """
        Test that an existing recycling bin can be deleted
        via a POST request to the admin dashboard.
        """
        # Create a test bin
        test_bin = Bin.objects.create(
            binIdentifier="BIN123",
            longitude=10.1234,
            latitude=20.5678
        )
        # Ensure the bin exists
        self.assertTrue(Bin.objects.filter(binIdentifier="BIN123").exists())

        # Delete the bin
        response = self.client.post(
            reverse('admin-dashboard'),
            {
                'bin_identifier': "BIN123"
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bin.objects.filter(binIdentifier="BIN123").exists())


class ManageBlockTests(TestCase):
    """
    Test suite for managing the blocks via the admin dashboard
    """
    def setUp(self):
        """
        Set up an admin user and log in to the test client 
        for accessing the admin dashboard.
        """
        admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpassword',
            is_superuser=True,
            is_staff=True
        )
        self.client.login(username='adminuser', password='adminpassword')

    def test_edit_existing_block(self):
        """
        Test that an existing block can be successfully edited 
        via a POST request to the admin dashboard.
        """
        # Create a test block
        block = Block.objects.create(
            value=50,
            cost=100
        )

        # Edit the block using the form
        response = self.client.post(
            reverse('admin-dashboard'),
            {
                'form_type': 'edit_block',
                'blockID': block.blockID,
                'value': 75,
                'cost': 150
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Refresh block from database and verify changes
        block.refresh_from_db()
        self.assertEqual(block.value, 75)
        self.assertEqual(block.cost, 150)


class ManageUsers(TestCase):
    """
    Test suite for managing user roles via the admin dashboard.
    """

    def setUp(self):
        """
        Set up an admin user and log in to the test client
        for accessing the admin dashboard.
        """
        admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpassword',
            is_superuser=True,
            is_staff=True
        )
        self.client.login(username='adminuser', password='adminpassword')

    def test_updating_existing_users_role(self):
        """
        Test that an existing user's role can be updated successfully
        via a POST request to the admin dashboard.
        """
        # Create a test user
        test_user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='user'
        )

        # Update the user's role to 'admin' using the form
        response = self.client.post(
            reverse('admin-dashboard'),
            {
                'form_type': 'edit_user',
                'user_id': test_user.id,
                'role': 'admin'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Refresh test_user from database and verify the role was updated
        test_user.refresh_from_db()
        self.assertEqual(test_user.role, 'admin')
