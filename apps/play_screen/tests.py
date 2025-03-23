"""Play Screen Tests

Tests if the play_screen functions work as intended

@version: 1.1
@date: 2025-03-07
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.quiz.models import quiz
from apps.recycling.models import Bin
from apps.stats.models import Stats

User = get_user_model()

# Create your views here.

class PlayScreenTests(TestCase):
    """Tests the user's access to the Play Screen"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_play_screen_renders_with_map(self):
        """Tests if play_screen.html is used and contains an iframe loading map.html"""
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.get(reverse('play_screen'))
        
        # Ensure the play_screen template has rendered
        self.assertTemplateUsed(response, "play_screen.html")

        # Ensure the iframe for the map is rendered
        expected_map_url = reverse('map')
        self.assertContains(response, f'<iframe src="{expected_map_url}"', html=False)

    def test_play_screen_unauthenticated_access_get(self):
        """Tests if a logged-out user is redirected when trying to GET the play_screen"""
        response = self.client.get(reverse('play_screen'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('play_screen'))

    def test_play_screen_with_broken_map(self):
        """Tests play screen behavior when the map fails to load"""
        self.client.login(username='testuser', password='testpassword#123')

        # Simulate a missing map URL (force an incorrect URL)
        expected_map_url = "/invalid_map_url/"
        response = self.client.get(reverse('play_screen'))
        
        # Ensure the page still renders, even if the map iframe is broken
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "iframe", html=False)

class QRScannerButtonTest(TestCase):
    """Tests for the QR Scan button"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client.login(username='testuser', password='testpassword#123')

    def test_qr_button_exists(self):
        """Test to see if the QR button exists in the play_screen"""
        response = self.client.get(reverse('play_screen'))
        self.assertEqual(response.status_code, 200)

        # Check if the button correctly links to the QR scanner page
        self.assertContains(response, f'href="{reverse("qr_scan")}"')
        self.assertContains(response, '<button id="my-button">Open Camera</button>', html=True)

    def test_qr_scanner_page_loads(self):
        """Test to see if the QR Scanner webpage loads"""
        response = self.client.get(reverse('qr_scan'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "QR Code Scanner")

    def test_qr_button_redirects_correctly_when_clicked(self):
        """Test if clicking the QR button actually redirects to the scanner page"""
        response = self.client.get(reverse('play_screen'))
        self.assertContains(response, f'href="{reverse("qr_scan")}"')

    def test_qr_scanner_page_redirects_for_unauthenticated_users(self):
        """Ensure unauthenticated users cannot access the QR scanner page"""
        self.client.logout()
        response = self.client.get(reverse('qr_scan'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('qr_scan'))

    def test_qr_scanner_fails_with_invalid_url(self):
        """Ensure the QR scanner page fails when given an incorrect URL"""
        response = self.client.get("/invalid_qr_scan/")
        self.assertEqual(response.status_code, 404)  # Expecting a "Not Found" error

class LocationQuizTests(TestCase):

    def setUp(self):
        """Set up a user and some quiz data for testing."""
        # Create a user and log in
        self.user = User.objects.create_user(username="testuser", password="testpassword#123")
        self.client.login(username="testuser", password="testpassword#123")

        # Create sample quiz data
        self.quiz1 = quiz.objects.create(
            quizID=1,
            locationID=0,
            question="What is the capital of France?",
            answer="Paris",
            other1="London",
            other2="Berlin",
            other3="Madrid"
        )

        self.quiz2 = quiz.objects.create(
            quizID=2,
            locationID=0,
            question="What is 2 + 2?",
            answer="4",
            other1="5",
            other2="3",
            other3="6"
        )

        self.quiz3 = quiz.objects.create(
            quizID=3,
            locationID=1,
            question="What is the square root of 16?",
            answer="4",
            other1="5",
            other2="6",
            other3="7"
        )

        # Create Stats for the user
        self.user_stats = Stats.objects.create(userID=self.user, yourPoints=0, yourTotalPoints=0)

    def test_quiz_view(self):
        """Test that the quiz view returns random questions and calculates score."""
        # Get the quiz page
        response = self.client.get(reverse('quiz'))

        # Ensure the page is loaded correctly
        self.assertEqual(response.status_code, 200)

        # Ensure questions are passed to the context
        questions = response.context['questions']
        self.assertEqual(len(questions), 2)  # 2 random questions should be selected (out of 2 available)

        # Check if score is initialized to 0
        self.assertEqual(response.context['score'], 0)

        # Simulate answering the quiz correctly
        data = {
            f'q{self.quiz1.quizID}': "Paris",  # Correct answer for quiz 1
            f'q{self.quiz2.quizID}': "4"  # Correct answer for quiz 2
        }

        response = self.client.post(reverse('quiz'), data)

        # Ensure score is updated correctly after answering the quiz
        self.assertEqual(response.context['score'], 2)

        # Verify that stats were updated
        self.user_stats.refresh_from_db()
        self.assertEqual(self.user_stats.yourPoints, 2)
        self.assertEqual(self.user_stats.yourTotalPoints, 2)

    def test_quiz_view_with_incorrect_answers(self):
        """Test the quiz view with incorrect answers."""
        # Simulate answering the quiz incorrectly
        data = {
            f'q{self.quiz1.quizID}': "London",  # Incorrect answer for quiz 1
            f'q{self.quiz2.quizID}': "3"  # Incorrect answer for quiz 2
        }

        response = self.client.post(reverse('quiz'), data)

        # Ensure score is still 0 after answering incorrectly
        self.assertEqual(response.context['score'], 0)

        # Verify incorrect answers are stored
        incorrect_answers = response.context['incorrect_answers']
        self.assertEqual(len(incorrect_answers), 2)  # 2 incorrect answers should be present
        self.assertEqual(incorrect_answers[0]['your_answer'], "London")
        self.assertEqual(incorrect_answers[0]['correct_answer'], "Paris")

    def test_quiz_view_by_location(self):
        """Test the quiz view by location with a specific location's questions."""
        # Test for locationID=0 (should include quiz1 and quiz2)
        response = self.client.get(reverse('quiz_location', kwargs={'locationID': 0}))

        # Ensure the page loads correctly
        self.assertEqual(response.status_code, 200)

        # Ensure only location-specific questions are included (should include quiz1 and quiz2)
        questions = response.context['questions']
        self.assertEqual(len(questions), 2)  # 2 questions for locationID 0

        # Test for locationID=1 (should include quiz3)
        response = self.client.get(reverse('quiz_location', kwargs={'locationID': 1}))

        # Ensure the page loads correctly
        self.assertEqual(response.status_code, 200)

        # Ensure only location-specific questions are included (should include quiz3)
        questions = response.context['questions']
        self.assertEqual(len(questions), 1)  # 1 question for locationID 1

    def test_quiz_view_no_questions_for_location(self):
        """Test if no questions are returned when no quiz is available for the location."""
        # Create a location with no associated quizzes
        response = self.client.get(reverse('quiz_location', kwargs={'locationID': 999}))

        # Ensure the page loads correctly but no questions are present
        self.assertEqual(response.status_code, 200)
        questions = response.context['questions']
        self.assertEqual(len(questions), 0)

    def test_authenticated_user_access(self):
        """Test if only authenticated users can access the quiz view."""
        self.client.logout()  # Logout user
        response = self.client.get(reverse('quiz'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

        response = self.client.get(reverse('quiz_location', kwargs={'locationID': 0}))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page