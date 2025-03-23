from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()

class AccessControlTests(TestCase):
    def setUp(self):
        self.normal_user = User.objects.create_user(username='normal_user', password='password')
        self.gamekeeper_user = User.objects.create_user(username='gamekeeper_user', password='password', role='gamekeeper')
        self.admin_user = User.objects.create_user(username='admin_user', password='password', role='admin')


    def test_normal_user_redirected(self):
        self.client.login(username='normal_user', password='password')
        response = self.client.get('/admin-dashboard/')
        self.assertRedirects(response, '/accounts/login/?next=/admin-dashboard/', fetch_redirect_response=False)

    def test_gamekeeper_user_access(self):
        self.client.login(username='gamekeeper_user', password='password')
        response = self.client.get('/admin-dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_admin_user_access(self):
        self.client.login(username='admin_user', password='password')
        response = self.client.get('/admin-dashboard/')
        self.assertEqual(response.status_code, 200)
