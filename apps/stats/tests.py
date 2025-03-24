"""Tests for the Stats App

Tests if the stats page can display the user's scores correctly

@version: 1.1
@date: 2025-03-22
@author: Sandy Hay & Edward Pratt
"""

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
    """Tests if the statistics page correctly displays values, including edge cases"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client.login(username='testuser', password='testpassword#123')

    def test_statistics_page_displays_zero_values_for_new_users(self):
        """Ensure new users with no stats see zero values"""
        response = self.client.get(reverse('stats'))
        self.assertContains(response, "0")  # Expecting default zero values

    def test_statistics_page_displays_correct_values(self):
        """Check if the statistics page correctly shows user stats"""
        stats = apps.stats.models.Stats.objects.create(
            userID=self.user,
            yourTotalPoints=10,
            plasticRecycled=50,
            metalRecycled=30,
            paperRecycled=40,
            packagingRecycled=20
        )

        response = self.client.get(reverse('stats'))
        expected_plastic_saved = (stats.plasticRecycled * 0.02) * 0.8
        expected_co2_saved = (
            (stats.plasticRecycled * 0.02) * 1.5 +
            (stats.metalRecycled * 0.05) * 2.5 +
            (stats.paperRecycled * 0.015) * 1.3 +
            (stats.packagingRecycled * 0.03) * 1.1
        )

        self.assertContains(response, "10")  # Check points
        self.assertContains(response, f"{expected_plastic_saved}")  # Plastic saved
        self.assertContains(response, f"{expected_co2_saved}")  # CO₂ saved

    def test_statistics_page_handles_large_values(self):
        """Test if large numbers are correctly displayed"""
        stats = apps.stats.models.Stats.objects.create(
            userID=self.user,
            yourTotalPoints=999999,
            plasticRecycled=999999,
            metalRecycled=999999,
            paperRecycled=999999,
            packagingRecycled=999999
        )
        response = self.client.get(reverse('stats'))
        self.assertContains(response, "999999")

    def test_statistics_page_handles_null_values(self):
        """Ensure null values do not break the page"""
        stats = apps.stats.models.Stats.objects.create(userID=self.user)
        response = self.client.get(reverse('stats'))
        self.assertContains(response, "0")  # Expecting fallback values (0)

# Class for testing quiz submission
class EarnPointsFromQuiz(TestCase):
    """Tests for Stats table displaying updated stats after user completes quiz"""
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

    def test_submit_quiz_with_no_answer(self):
        """Tests form submission with no answer"""
        url = reverse(quiz_view)
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        points = apps.stats.models.Stats.objects.get(userID=self.user).yourTotalPoints
        self.assertEqual(points, 0)  # No increase in points

    def test_submit_quiz_with_wrong_answer(self):
        """Tests submission with an incorrect answer"""
        url = reverse(quiz_view)
        data = {
            'q1': 'WrongAnswer1'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        points = apps.stats.models.Stats.objects.get(userID=self.user).yourTotalPoints
        self.assertEqual(points, 0)  # No points for wrong answer

    def test_submit_quiz_with_multiple_attempts(self):
        """Tests if points accumulate after multiple quiz submissions"""
        url = reverse(quiz_view)
        data = {
            'q1': 'CorrectAnswer'
        }

        for _ in range(3):  # Three correct answers
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)

        points = apps.stats.models.Stats.objects.get(userID=self.user).yourTotalPoints
        self.assertEqual(points, 3)  # Should be 3 after 3 correct attempts



