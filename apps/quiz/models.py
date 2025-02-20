from django.db import models

# Create your models here.
class quiz(models.Model):
    quizID = models.AutoField(primary_key=True)
    question = models.CharField(max_length=512)
    answer = models.CharField(max_length=512)
    other1 = models.CharField(max_length=512)
    other2 = models.CharField(max_length=512)
    other3 = models.CharField(max_length=512)


    def __str__(self):
        return self.quizID


class quizTimeout(models.Model):
    timeoutID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    quizID = models.ForeignKey('quiz', on_delete=models.CASCADE)
    timeout = models.DateTimeField()

    def __str__(self):
        return self.timeoutID
