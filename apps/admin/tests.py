from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from apps.quiz.models import quiz
from apps.play_screen.models import QuizLocation

User = get_user_model()

class AccessControlTests(TestCase):
    def setUp(self):
        self.normal_user = User.objects.create_user(username='normal_user', password='password')
        self.gamekeeper_user = User.objects.create_user(username='gamekeeper_user', password='password', role='gamekeeper')
        self.admin_user = User.objects.create_user(username='admin_user', password='password', role='admin')


    def test_normal_user_redirected(self):
        self.client.login(username='normal_user', password='password')
        response = self.client.get('/admin-dashboard/')
        self.assertRedirects(response, '/accounts/login/?next=/admin-dashboard/', fetch_redirect_response=False)

    def test_gamekeeper_user_access(self):
        self.client.login(username='gamekeeper_user', password='password')
        response = self.client.get('/admin-dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_admin_user_access(self):
        self.client.login(username='admin_user', password='password')
        response = self.client.get('/admin-dashboard/')
        self.assertEqual(response.status_code, 200)


class AdminDashboardTests(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username='admin', password='pass123', role='admin'
        )
        # Create a test client and log in as the admin user
        self.client = Client()
        self.client.login(username='admin', password='pass123')


    def test_get_admin_dashboard(self):
        # Use reverse to resolve the URL name for the admin dashboard
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin.html')
        # Verify that context contains expected keys (e.g., 'questions', 'locations')
        self.assertIn('questions', response.context)

class QuizQuestionsTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin', password='pass123', role='admin', is_superuser=True, is_staff=True,
        )
        # Create a test client and log in as the admin user
        self.client = Client()
        self.client.login(username='admin', password='pass123')

    def test_add_quiz_question(self):
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

    def test_delete_quiz_location(self):
        """
        Test deleting an existing quiz location along with its associated quiz questions.
        """
        # Create the admin user and log in
        admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpassword',
            is_superuser=True,
            is_staff=True
        )
        self.client.login(username='adminuser', password='adminpassword')

        # Create a location
        location = QuizLocation.objects.create(
            longitude=12.3456,
            latitude=65.4321,
            locationName="Location to Delete"
        )

        # Create associated quiz questions
        for i in range(3):  # Add 3 questions for this location
            quiz.objects.create(
                locationID=location.locationID,
                question=f"Question {i + 1}?",
                answer=f"Answer {i + 1}",
                other1=f"Incorrect {i + 1}_1",
                other2=f"Incorrect {i + 1}_2",
                other3=f"Incorrect {i + 1}_3"
            )

        # Ensure the location and associated questions exist
        self.assertTrue(QuizLocation.objects.filter(locationName="Location to Delete").exists())
        self.assertEqual(quiz.objects.filter(locationID=location.locationID).count(), 3)

        # Delete the location
        response = self.client.post(
            reverse('admin-dashboard'),
            {'location_name': "Location to Delete"},
            follow=True
        )

        # Assert the response status and ensure the location and questions are deleted
        self.assertEqual(response.status_code, 200)
        self.assertFalse(QuizLocation.objects.filter(locationName="Location to Delete").exists())
        self.assertEqual(quiz.objects.filter(locationID=location.locationID).count(), 0)
