"""Tests for the leaderboard page

Tests to see if the user can access the leaderboard page, if the leaderboard is
displayed correctly and that the new players can be added to the leaderboard.
It must also verify that the leaderboard can be sorted by the user's score.

@version: 1.0
@date: 2021-04-07
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class LeaderboardPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_authenticated_leaderboard_user_access(self):
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.post(reverse('leaderboardpage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard.html')

    def test_unauthenticated_leaderboard_user_access(self):
        response = self.client.post(reverse('leaderboardpage'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('leaderboardpage'))

# class LeaderboardTests(TestCase):
#     def setUp(self):
