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
            username='admin', password='pass123', role='admin'
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



class QuizLocationsTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin', password='pass123', role='admin'
        )
        # Create a test client and log in as the admin user
        self.client = Client()
        self.client.login(username='admin', password='pass123')


    def test_add_quiz_location_with_questions(self):
        """
        Test adding a new quiz location along with its 5 quiz questions.
        """
        location_data = {
            # Location fields
            'longitude': '12.3456',
            'latitude': '65.4321',
            'location_name': 'Test Location',
        }
        # Add data for 5 quiz questions; each question has one correct answer and three incorrect answers.
        for i in range(1, 6):
            location_data[f'question_{i}'] = f"Test Question {i}?"
            location_data[f'answer_{i}'] = f"Correct Answer {i}"
            location_data[f'incorrect_{i}_1'] = f"Incorrect Answer {i}-1"
            location_data[f'incorrect_{i}_2'] = f"Incorrect Answer {i}-2"
            location_data[f'incorrect_{i}_3'] = f"Incorrect Answer {i}-3"

        response = self.client.post(reverse('admin-dashboard'), location_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check that the new location has been added
        self.assertTrue(QuizLocation.objects.filter(locationName='Test Location').exists())
        new_location = QuizLocation.objects.get(locationName='Test Location')

        # Check that 5 quiz questions have been created for this location.
        questions = quiz.objects.filter(locationID=new_location.locationID)
        self.assertEqual(questions.count(), 5)



    def test_edit_quiz_location(self):
        """
        Test editing an existing quiz location.
        """
        # Create a location to edit.
        location = QuizLocation.objects.create(
            longitude="12.3456",
            latitude="65.4321",
            locationName="Original Location"
        )
        # Prepare data for editing (note the inclusion of 'form_type' as expected by the view).
        edit_data = {
            'form_type': 'edit_location',
            'location_id': location.locationID,
            'longitude': "98.7654",
            'latitude': "54.3210",
            'location_name': "Updated Location"
        }
        response = self.client.post(reverse('admin-dashboard'), edit_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Refresh the object from the database and verify the changes.
        location.refresh_from_db()
        self.assertEqual(location.longitude, "98.7654")
        self.assertEqual(location.latitude, "54.3210")
        self.assertEqual(location.locationName, "Updated Location")
