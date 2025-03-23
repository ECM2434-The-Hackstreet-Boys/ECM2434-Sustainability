"""Play Screen Tests

Tests if the play_screen functions work as intended

@version: 1.1
@date: 2025-03-07
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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