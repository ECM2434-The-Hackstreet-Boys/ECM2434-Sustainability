"""Play Screen Tests

Tests if the play_screen functions work as intended

@version: 1.0
@date: 2025-03-07
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.

class PlayScreenTests(TestCase):
    """Tests the user's access to the Play Screen"""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_play_screen_renders_with_map(self):
        """Tests if play_screen.html is used and contains an iframe loading map.html"""
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.get(reverse('play_screen'))

        # Ensure the play_screen template has rendered in
        self.assertTemplateUsed(response, "play_screen.html")

        # Ensure the iframe for the map is rendered as well
        expected_map_url = reverse('map')
        self.assertContains(response, f'<iframe src="{expected_map_url}"', html=False)

    def test_play_screen_unauthenticated_access(self):
        """Tests if a logged out user gets redirected after attempting to access the play_screen"""
        response = self.client.post(reverse('stats'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('stats'))

class QRScannerButtonTest(TestCase):
    """Tests for the QR Scan button"""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client.login(username='testuser', password='testpassword#123')

    def test_qr_button_exists(self):
        """Test to see if the button exists in the play_screen"""
        response = self.client.get(reverse('play_screen'))

        self.assertEqual(response.status_code, 200)

        # Checks if the button contains the view of the QR Scanner webpage
        self.assertContains(response, f'href="{reverse("qr_scan")}"')
        self.assertContains(response, '<button id="my-button">Open Camera</button>', html=True)

    def test_qr_scanner_page_loads(self):
        """Test to see if the Qr Scanner webpage does load"""
        response = self.client.get(reverse('qr_scan'))

        # Ensure the page loads successfully
        self.assertEqual(response.status_code, 200)

        # Optionally, check if the QR scanner page contains expected content
        self.assertContains(response, "QR Code Scanner")  # Modify based on the actual page content
