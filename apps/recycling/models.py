# Author: Edward Pratt, Ethan Clapham
from django.db import models

# Model for storing the bins, qr codes and locations
class Bin(models.Model):
    binID = models.AutoField(primary_key=True)
    location = models.CharField(max_length=512)
    qrCode = models.IntegerField()

    def __str__(self):
        return self.binID