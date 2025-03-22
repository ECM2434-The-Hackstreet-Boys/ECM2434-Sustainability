"""Tests for the Quiz app

Tests the quiz functions and view if a user can earn points from getting
correct answers on the quizzes

@version: 1.0
@date: 2025-03-07
@author: Sandy Hay
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.stats.models import Stats
from apps.quiz.models import quiz

User = get_user_model()

# Create your tests here.

class QuizPageTest(TestCase):
    """Tests for the Quiz Page"""
    def setUp(self):
        """Set up a test user and sample quiz questions"""
        self.user = User.objects.create_user(username="testuser", password="testpassword#123")

        # Create sample quiz questions
        self.quiz1 = quiz.objects.create(
            quizID=1, question="Test1", answer="CorrectAnswer1", other1="WrongAnswer1_1", other2="WrongAnswer1_2", other3="WrongAnswer1_3"
            )
        self.quiz2 = quiz.objects.create(
            quizID=2, question="Test2", answer="CorrectAnswer2", other1="WrongAnswer2_1", other2="WrongAnswer2_2", other3="WrongAnswer2_3"
            )

    def test_authenticated_Quiz_Page_Access(self):
        """Test that an authenticated user can access the quiz page"""
        self.client.login(username="testuser", password="testpassword#123")  # Log in user
        response = self.client.get(reverse("quiz"))  # Update with actual URL name

        self.assertEqual(response.status_code, 200)  # Page should load
        self.assertTemplateUsed(response, "quiz.html")  # Ensure correct template is used

    def test_unauthenticated_Quiz_Page_Access(self):
        """Test that an unauthenticated user is redirected from the quiz page"""
        response = self.client.get(reverse("quiz"))  # No login

        # Check for redirect to login page (Django default behavior)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(response.url.startswith(reverse("login")))  # Ensure redirection to login


    def test_quiz_page_renders(self):
        """Tests if the quiz page renders for a logged-in user"""
        self.client.login(username="testuser", password="testpassword#123")
        response = self.client.get(reverse("quiz"))  # Update with your actual URL name

        # Ensure the page loads successfully
        self.assertEqual(response.status_code, 200)

        # Ensure the correct template is used
        self.assertTemplateUsed(response, "quiz.html")

        # Check if sample questions exist in the rendered page
        self.assertContains(response, "CorrectAnswer1")
        self.assertContains(response, "WrongAnswer2_2")

class QuizAnswerTest(TestCase):
    """Tests if the quiz answers function work and updates player points"""
    def setUp(self):
        """Set up test user, stats, and quiz questions"""
        self.user = User.objects.create_user(username="testuser", password="testpassword#123")
        self.client.login(username="testuser", password="testpassword#123")

        # Create sample quiz questions
        self.q1 = quiz.objects.create(
            quizID=1, question="What is 2+2?", answer="4", other1="3", other2="5", other3="6"
        )
        self.q2 = quiz.objects.create(
            quizID=2, question="What is the capital of France?", answer="Paris", other1="London", other2="Berlin", other3="Madrid"
        )

        # Ensure Stats model exists for the user and initialize points if not created
        self.stats, created = Stats.objects.get_or_create(userID=self.user)
        self.stats.yourPoints = 0
        self.stats.yourTotalPoints = 0
        self.stats.save()

    def test_quiz_score_updates_correctly(self):
        """Tests if answering quiz questions updates the user's points correctly"""
        # Submit quiz answers
        response = self.client.post(reverse("quiz"), {
            "q1": "4",  # Correct answer for first question
            "q2": "London",  # Incorrect answer for second question
        })

        # Retrieve the updated points after quiz submission
        updated_points = Stats.objects.get(userID=self.user).yourPoints

        # The user answered 1 question correctly, so points should increase by 1
        self.assertEqual(updated_points, 1)

        # Ensure the quiz page still renders correctly after submission
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz.html")

        # Optionally, verify feedback for incorrect answers
        self.assertContains(response, "Incorrect Answers")
        self.assertContains(response, "<strong>Question:</strong> What is the capital of France?")
        self.assertContains(response, "<strong style = \"color: red;\">Answer:</strong> London")  # User's incorrect answer
        self.assertContains(response, "<strong style = \"color: green;\">Correct Answer:</strong> Paris")  # Correct answer
