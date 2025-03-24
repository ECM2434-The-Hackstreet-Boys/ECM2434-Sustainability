"""
Model for the recycling page

@Author: Ethan Clapham, Edward Pratt
"""
from django.db import models

class Bin(models.Model):
    """Model for storing the bins, qr codes and locations"""
    binID = models.AutoField(primary_key=True)
    binIdentifier = models.CharField(max_length=50, default="No identifier")
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

