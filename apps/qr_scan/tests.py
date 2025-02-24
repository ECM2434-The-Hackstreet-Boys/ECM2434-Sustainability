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
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')

    def test_authenticated_qr_scan_user_access(self):
        """Tests if an authenticated user can access the QR Scan page"""
        self.client.login(username='testuser', password='testpassword#123')
        response = self.client.post(reverse('qr_scan'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qr_scan.html')

    def test_unauthenticated_qr_scan_user_access(self):
        """Tests if an unauthenticated user cannot access the QR Scan page"""
        response = self.client.post(reverse('qr_scan'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('qr_scan'))

class QRScanPageTests(TestCase):
    """Tests the QR Scan functionality"""
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword#123')

    def test_qr_scan_contains_reader_div(self):
        """Test that the page contains the reader"""
        response = self.client.get(reverse('qr_scan'))
        self.assertContains(response, '<div id="reader"')

    def test_qr_scan_page_result_paragraph(self):
        """Test that the page contains the result display paragraph"""
        response = self.client.get(reverse('qr_scan'))
        self.assertContains(response, '<p id="result">')

    def test_qr_scan_page_javascript_functions(self):
        """Test that the page includes the javascript functions for QR Code scanning"""
        response = self.client.get(reverse('qr_scan'))
        self.assertContains(response, "function onScanSuccess")
        self.assertContains(response, "function onScanFailure")
        self.assertContains(response, "html5QrcodeScanner.render(onScanSuccess, onScanFailure)")
        self.assertContains(response, "Scanned Code:")



    
