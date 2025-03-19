# Author: Edward Pratt, Ethan Clapham
from django.db import models

# Model for storing the bins, qr codes and locations
class Bin(models.Model):
    binID = models.AutoField(primary_key=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    qrCode = models.IntegerField()

    def __str__(self):
        return self.binID