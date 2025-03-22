# Author: Edward Pratt, Sandy Hay

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

import apps.stats.models
from apps.quiz.models import quiz
from apps.quiz.views import quiz_view

# Create your tests here.


User = get_user_model()

# Class for testing if statistics page renders
class StatisticsPageTests(TestCase):
    """Tests user access to the Statistics Page"""
    # Sets up the test by creating a user
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_statistics_page_authenticated_access(self):
        """Tests if the user can access the statistic page while being logged in"""
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.post(reverse('stats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statistics.html')

    def test_statistics_page_unauthenticated_access(self):
        """Tests if an logged out user gets redirected after attempting to access the statistics page"""
        response = self.client.post(reverse('stats'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('stats'))

    def test_statistics_page_renders(self):
        """Tests if the statistics page renders in when loaded in"""
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.post(reverse('stats'))
        self.assertContains(response, "Your Points")
        self.assertContains(response, "KG of CO2 Saved")
        self.assertContains(response, "KG of Plastic Saved")
    
class StatisticsTests(TestCase):
    """Tests if the statistics page shows the values properly"""

    def setUp(self):
        # Create test user and log in
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client.login(username='testuser', password='testpassword#123')

        # Create a Stats object with sample data
        self.stats = apps.stats.models.Stats.objects.create(
            userID=self.user,
            yourPoints=10,
            plasticRecycled=50,   # 50 items * 0.02 kg = 1.0 kg
            metalRecycled=30,     # 30 items * 0.05 kg = 1.5 kg
            paperRecycled=40,     # 40 items * 0.015 kg = 0.6 kg
            packagingRecycled=20  # 20 items * 0.03 kg = 0.6 kg
        )

    def test_statistics_page_displays_correct_values(self):
        """Check if the statistics page shows updated points, plastic saved, and CO₂ saved"""
        response = self.client.get(reverse('stats'))

        # Check if the page loads successfully
        self.assertEqual(response.status_code, 200)

        # Calculate expected values
        expected_plastic_saved = (self.stats.plasticRecycled * 0.02) * 0.8  # 1.0 * 0.8 = 0.8 kg
        expected_co2_saved = (
            (self.stats.plasticRecycled * 0.02) * 1.5 +  # Plastic CO₂ savings
            (self.stats.metalRecycled * 0.05) * 2.5 +    # Metal CO₂ savings
            (self.stats.paperRecycled * 0.015) * 1.3 +   # Paper CO₂ savings
            (self.stats.packagingRecycled * 0.03) * 1.1  # Packaging CO₂ savings
        )  # = 0.8*1.5 + 1.5*2.5 + 0.6*1.3 + 0.6*1.1 = 1.2 + 3.75 + 0.78 + 0.66 = 6.39 kg

        # Verify if the correct values are displayed
        self.assertContains(response, "10")  # Check points
        self.assertContains(response, f"{expected_plastic_saved}")  # Check plastic saved
        self.assertContains(response, f"{expected_co2_saved}")  # Check CO₂ saved

# Class for testing quiz submission
class EarnPointsFromQuiz(TestCase):

    # Sets up the test by creating a user and quiz object
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.quiz = quiz.objects.create(question="Test", answer="CorrectAnswer", other1="WrongAnswer1", other2="WrongAnswer2", other3="WrongAnswer3")
        self.client.login(username='testuser', password='testpassword#123')


    # Tests the submission of a quiz form
    def test_submit_quiz_form(self):
        url = reverse(quiz_view)
        data = {
            'q1': 'CorrectAnswer'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


    # Tests that the user's points increase after submitting a quiz form
    def test_check_points_increase(self):
        url = reverse(quiz_view)
        data = {
            'q1': 'CorrectAnswer'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        points = apps.stats.models.Stats.objects.get(userID=self.user).yourPoints
        self.assertTrue(points == 1)


