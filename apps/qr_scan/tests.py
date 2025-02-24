"""Tests for the QR Scan app

The QR Scan app allows users to scan QR codes to access the garden

@version: 1.0
@date: 2021-04-07
@author: Sandy Hay
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.

class QRScanUserAccessTests(TestCase):
    """Test the user's access to the QR Scan page"""
    def setUp(self):
        """Sets up a user for testing purposes"""
        self.user = User.objects.create_user(username='testuser', password='testpassword#123') # Create a user

    def test_authenticated_qr_scan_user_access(self):
        """Tests if an authenticated user can access the QR Scan page"""
        self.client.login(username='testuser', password='testpassword#123') # Login the user
        response = self.client.post(reverse('qr_scan')) # Access the QR Scan page
        self.assertEqual(response.status_code, 200) # Should return 200 (OK) status code as the user is authenticated
        self.assertTemplateUsed(response, 'qr_scan.html') # Check if the correct template is used

    def test_unauthenticated_qr_scan_user_access(self):
        """Tests if an unauthenticated user cannot access the QR Scan page"""
        response = self.client.post(reverse('qr_scan'))
        self.assertEqual(response.status_code, 302) # Should return 302 (redirect) as the user is not authenticated
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('qr_scan')) # Redirects to login page and returns to QR Scan page

class QRScanPageTests(TestCase):
    """Tests the QR Scan functionality"""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client = Client() # Create a test client
        self.client.login(username='testuser', password='testpassword#123') # Login the user

    def test_qr_scan_contains_reader_div(self):
        """Test that the page contains the reader"""
        response = self.client.get(reverse('qr_scan'))
        self.assertContains(response, '<div id="reader"') # Check if the reader div is present

    def test_qr_scan_page_result_paragraph(self):
        """Test that the page contains the result display paragraph"""
        response = self.client.get(reverse('qr_scan'))
        self.assertContains(response, '<p id="result">') # Check if the result paragraph is present

    def test_qr_scan_page_javascript_functions(self):
        """Test that the page includes the javascript functions for QR Code scanning"""
        response = self.client.get(reverse('qr_scan'))
        self.assertContains(response, "function onScanSuccess") # Check if the function for successful scan is present
        self.assertContains(response, "function onScanFailure") # Check if the function for failed scan is present
        self.assertContains(response, "html5QrcodeScanner.render(onScanSuccess, onScanFailure)") # Check if the render function is present
        self.assertContains(response, "Scanned Code:") # Check if the printed result of the scanned code exists