from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

import apps.stats.models
from apps.quiz.models import quiz
from apps.quiz.views import quiz_view

# Create your tests here.


User = get_user_model()

class EarnPointsFromQuiz(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword#123')
        self.quiz = quiz.objects.create(question="Test", answer="CorrectAnswer", other1="WrongAnswer1", other2="WrongAnswer2", other3="WrongAnswer3")
        self.client.login(username='testuser', password='testpassword#123')


    def test_submit_quiz_form(self):
        url = reverse(quiz_view)
        data = {
            'q1': 'CorrectAnswer'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_check_points_increase(self):
        url = reverse(quiz_view)
        data = {
            'q1': 'CorrectAnswer'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        points = apps.stats.models.Stats.objects.get(userID=self.user).yourPoints
        self.assertTrue(points == 1)


