"""Tests for the leaderboard page

Tests to see if the user can access the leaderboard page, if the leaderboard is
displayed correctly and that the new players can be added to the leaderboard.

@version: 1.0
@date: 2021-04-07
@author: Sandy Hay
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.apps import apps

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

class LeaderboardUserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword#123')

        Stats = apps.get_model('stats', 'Stats')  # Correct way to get model
        self.stats = Stats.objects.create(userID=self.user, yourPoints=0)
    
    def test_user_in_leaderboard(self):
        response = self.client.get(reverse('leaderboardpage'))
        self.assertContains(response, 'testuser')

    def test_user_points_gained_on_leaderboard(self):
        self.stats.yourPoints += 10
        self.stats.save() # Save the updated points

        response = self.client.get(reverse('leaderboardpage')) # Changed from post() to get()
        self.assertContains(response, '10')

    # class LeaderboardfsfdTests(TestCase):


