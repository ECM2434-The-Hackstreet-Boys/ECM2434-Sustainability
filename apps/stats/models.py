from django.db import models

# Create your models here.


# Stats model to store relevant statistics for each user
class Stats(models.Model):
    statsID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    yourPoints = models.IntegerField(default=0)
    co2Saved = models.IntegerField(default=0)
    plasticSaved = models.IntegerField(default=0)



    def __str__(self):
        return self.statsID
