# Author: Edward Pratt, Ethan Clapham

from django.db import models

# Stats model to store relevant statistics for each user
class Stats(models.Model):
    statsID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    yourPoints = models.IntegerField(default=0)
    yourTotalPoints = models.IntegerField(default=0)
    packagingRecycled = models.IntegerField(default=0)
    plasticRecycled = models.IntegerField(default=0)
    metalRecycled = models.IntegerField(default=0)
    paperRecycled = models.IntegerField(default=0)

    def __str__(self):
        return self.statsID
