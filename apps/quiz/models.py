"""
Models for the quiz app

@Author: Edward Pratt
"""
from django.db import models

# Create your models here.

# Quiz model stores, question, answer and 3 other options
class quiz(models.Model):
    """
    Model to store quiz questions, answers, and multiple options.
    Attributes:
        quizID (AutoField): Unique identifier for each quiz.
        locationID (IntegerField): The location ID where the quiz is related (optional).
        question (CharField): The question to be displayed in the quiz.
        answer (CharField): The correct answer for the quiz.
        other1 (CharField): The first incorrect option.
        other2 (CharField): The second incorrect option.
        other3 (CharField): The third incorrect option.
    """
    quizID = models.AutoField(primary_key=True)
    locationID = models.IntegerField(null=True, blank=True, default=0)
    question = models.CharField(max_length=512)
    answer = models.CharField(max_length=512)
    other1 = models.CharField(max_length=512)
    other2 = models.CharField(max_length=512)
    other3 = models.CharField(max_length=512)

    def __str__(self):
        return str(self.quizID)

# QuizTimeout model stores the timeout for each quiz for each user
class quizTimeout(models.Model):
    """
    Model to store timeout data for each quiz attempted by a user.
    Attributes:
        timeoutID (AutoField): Unique identifier for each timeout record.
        userID (ForeignKey): The user who attempted the quiz.
        quizID (ForeignKey): The quiz that the timeout applies to.
        timeout (DateTimeField): The timestamp of the timeout for the quiz attempt.
    """
    timeoutID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    quizID = models.ForeignKey('quiz', on_delete=models.CASCADE)
    timeout = models.DateTimeField()

    def __str__(self):
        return str(self.timeoutID)
