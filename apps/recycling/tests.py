"""Recycling Tests

Tests if the user can correctly access the recycling form with the correct bin
ID and 

@version: 1.1
@date: 2025-03-22
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.stats.models import Stats
from apps.recycling.models import Bin

User = get_user_model()

# Create your tests here.

class RecyclingTests(TestCase):
    def setUp(self):
        """Set up test user and a bin location"""
        self.user = User.objects.create_user(username="testuser", password="testpassword#123")
        self.bin = Bin.objects.create(binID=1, latitude=50.1234, longitude=-3.5678)
        self.stats = Stats.objects.create(userID=self.user, packagingRecycled=0, plasticRecycled=0, metalRecycled=0, paperRecycled=0)

    def test_recycling_page_loads_successfully(self):
        """Ensure recycling page loads correctly for a valid bin ID"""
        self.client.login(username="testuser", password="testpassword#123")
        response = self.client.get(reverse("recycling", args=[self.bin.binID]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Recycling Bin Tracker</h1>")
        self.assertContains(response, '<form id = "recycling-form"')  # Ensure form is present

    def test_recycling_page_invalid_bin(self):
        """Ensure 404 is returned if a bin does not exist"""
        self.client.login(username="testuser", password="testpassword#123")
        response = self.client.get(reverse("recycling", args=[999]))  # Non-existent bin
        self.assertEqual(response.status_code, 404)

    def test_submit_recycling_updates_stats(self):
        """Ensure submitting recycling data updates the user’s stats correctly"""
        self.client.login(username="testuser", password="testpassword#123")
        response = self.client.post(reverse("submit_recycling"), {
            "food-packaging": "5",
            "plastic": "3",
            "metal": "2",
            "paper": "4"
        })

        self.stats.refresh_from_db()
        self.assertEqual(self.stats.packagingRecycled, 5)
        self.assertEqual(self.stats.plasticRecycled, 3)
        self.assertEqual(self.stats.metalRecycled, 2)
        self.assertEqual(self.stats.paperRecycled, 4)
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard

    def test_submit_recycling_invalid_data(self):
        """Ensure non-numeric data does not break the stats update"""
        self.client.login(username="testuser", password="testpassword#123")
        
        response = self.client.post(reverse("submit_recycling"), {
            "food-packaging": "invalid",
            "plastic": "NaN",
            "metal": "-5",
            "paper": "2"
        })
        
        self.stats.refresh_from_db()  # Refresh stats from database

        # Ensure invalid input did not update stats
        self.assertEqual(self.stats.packagingRecycled, 0)  # Should stay 0
        self.assertEqual(self.stats.plasticRecycled, 0)
        self.assertEqual(self.stats.metalRecycled, 0)
        self.assertEqual(self.stats.paperRecycled, 2)

        # Ensure redirection works
        self.assertRedirects(response, reverse("dashboard"))

    def test_submit_recycling_unauthenticated_user(self):
        """Ensure an unauthenticated user is redirected to login"""
        response = self.client.post(reverse("submit_recycling"), {
            "food-packaging": "3",
            "plastic": "2",
            "metal": "1",
            "paper": "5"
        })
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('submit_recycling'))

