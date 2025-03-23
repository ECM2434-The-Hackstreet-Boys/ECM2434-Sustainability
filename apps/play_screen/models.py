# Author: Ethan Clapham
from django.db import models

# Create your models here.
class QuizLocation(models.Model):
    locationID = models.AutoField(primary_key=True)
    locationName = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    quizID = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.quizID is None:
            super().save(*args, **kwargs)
            self.quizID = self.locationID
        super().save(*args, **kwargs)

    def __str__(self):
        return self.locationID
