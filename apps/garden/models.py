# Author:  Edward Pratt

import os.path

from django.db import models


# Helper function for garden pathing
def garden_file_path(instance, filename):
    return os.path.join('gardens', f'{instance.userID.username}_{instance.name}.json')


# Model for linking the user to their garden file, also stores a rating for gardens
class Garden(models.Model):
    gardenID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    file_path = models.FileField(upload_to=garden_file_path, null=True, blank=True)
    rating = models.FloatField(default=0)


    def __str__(self):
        return self.gardenID

# Model for linking the user to their inventory, containing which flowers they have and how many
class Inventory(models.Model):
    inventoryID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    blockID = models.ForeignKey('Block', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return self.inventoryID

# Model for the block, containing the name, cost, and value of the block
class Block(models.Model):
    blockID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    cost = models.IntegerField(default=0)
    value = models.IntegerField(default=0)