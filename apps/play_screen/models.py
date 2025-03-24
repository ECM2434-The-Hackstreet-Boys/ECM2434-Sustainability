"""
Model for the play screen app

@Author: Ethan Clapham
"""
from django.db import models

class QuizLocation(models.Model):
    """Model for storing quiz location details"""
    locationID = models.AutoField(primary_key=True)
    locationName = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    quizID = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Custom save method to set quizID based on locationID if quizID is not provided"""
        if self.quizID is None:
            super().save(*args, **kwargs)  # initial insert to DB to get locationID
            self.quizID = self.locationID
            super().save(update_fields=['quizID'])  # update quizID explicitly
        else:
            super().save(*args, **kwargs)  # normal updates thereafter
