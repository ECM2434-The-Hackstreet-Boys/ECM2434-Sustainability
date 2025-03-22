"""Tests for the leaderboard page

Tests to see if the user can access the leaderboard page, if the leaderboard is
displayed correctly and that the new players can be added to the leaderboard.

@version: 1.0
@date: 2025-03-07
@author: Sandy Hay
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()

# Create your tests here.
class LeaderboardPageTests(TestCase):
    """Tests the leaderboard page"""
    def setUp(self):
        """Sets up a user for testing purposes"""
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_authenticated_leaderboard_user_access(self):
        """Tests if an authenticated user can access the leaderboard page"""
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.post(reverse('leaderboardpage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard.html')

    def test_unauthenticated_leaderboard_user_access(self):
        """Tests if an unauthenticated user cannot access the leaderboard page"""
        response = self.client.post(reverse('leaderboardpage'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('leaderboardpage'))

class LeaderboardUserTests(TestCase):
    """Tests the leaderboard with a single user"""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword#123')

        Stats = apps.get_model('stats', 'Stats')
        self.stats = Stats.objects.create(userID=self.user, yourTotalPoints=0)
    
    def test_user_in_leaderboard(self):
        """Tests if the user is displayed in the leaderboard"""
        response = self.client.get(reverse('leaderboardpage'))
        self.assertContains(response, 'testuser')

    def test_user_points_gained_on_leaderboard(self):
        """Tests if the user's points are updated on the leaderboard"""
        self.stats.yourTotalPoints += 10
        self.stats.save() # Save the updated points

        response = self.client.get(reverse('leaderboardpage')) # Changed from post() to get()
        self.assertContains(response, '10')

class LeaderboardMultipleUsersTests(TestCase):
    """Tests the leaderboard with multiple users"""
    def setUp(self):
        """Sets up 3 users for testing purposes"""
        # Make 3 users
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword#1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword#2')
        self.user3 = User.objects.create_user(username='testuser3', password='testpassword#3')
        self.client = Client()
        self.client.login(username='testuser1', password='testpassword#1')

        Stats = apps.get_model('stats', 'Stats')
        self.stats1 = Stats.objects.create(userID=self.user1, yourTotalPoints=25)
        self.stats2 = Stats.objects.create(userID=self.user2, yourTotalPoints=18)
        self.stats3 = Stats.objects.create(userID=self.user3, yourTotalPoints=1)
    
    def test_multiple_users_in_leaderboard(self):
        """Tests if multiple users are displayed in the leaderboard"""
        response = self.client.get(reverse('leaderboardpage'))
        self.assertContains(response, '25')
        self.assertContains(response, '18')
        self.assertContains(response, '1')


