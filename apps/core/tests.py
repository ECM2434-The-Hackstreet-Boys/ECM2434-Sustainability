"""
Tests the main core parts of the webpage

@version: 1.0
@date: 2025-03-21
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class GDPRPrivacyPolicyTest(TestCase):
    """Tests for the GDPR Privacy Policy"""
    def test_GDPR_link_exists(self):
        """Tests if the GDPR Policy URL exists"""
        # Make a request to the main page (replace 'home' with your actual URL name if necessary)
        response = self.client.get(reverse('home'))  # Or replace 'home' with the actual URL name

        # Check if the link to the PDF exists on the page
        self.assertContains(response, '/static/resources/EcoWorld%20Privacy%20Policy.pdf')

