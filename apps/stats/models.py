"""
Model for the Stats page

@Author: Edward Pratt, Ethan Clapham
"""

from django.db import models

# Stats model to store relevant statistics for each user
class Stats(models.Model):
    """Model to store user recycling statistics and points.

    Attributes:
        statsID (AutoField): Primary key for the stats record.
        userID (ForeignKey): Reference to the associated user.
        yourPoints (IntegerField): Points earned for recycling activities.
        yourTotalPoints (IntegerField): Total accumulated points.
        packagingRecycled (IntegerField): Count of recycled packaging items.
        plasticRecycled (IntegerField): Count of recycled plastic items.
        metalRecycled (IntegerField): Count of recycled metal items.
        paperRecycled (IntegerField): Count of recycled paper items.
    """
    statsID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    yourPoints = models.IntegerField(default=0)
    yourTotalPoints = models.IntegerField(default=0)
    packagingRecycled = models.IntegerField(default=0)
    plasticRecycled = models.IntegerField(default=0)
    metalRecycled = models.IntegerField(default=0)
    paperRecycled = models.IntegerField(default=0)

    def __str__(self):
        return str(self.statsID)  # Ensure __str__ returns a string

