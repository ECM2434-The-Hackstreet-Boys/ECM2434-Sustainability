"""
Models for the garden

@Author: Edward Pratt
"""

import os.path

from django.db import models

def garden_file_path(instance, filename):
    """Helper function for garden pathing"""
    return os.path.join('gardens', f'{instance.userID.username}_{instance.name}.json')

class Garden(models.Model):
    """Model for linkiing the user to their garden file, also stores a rating for garden"""
    gardenID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    file_path = models.FileField(upload_to=garden_file_path, null=True, blank=True)
    rating = models.FloatField(default=0)


    def __str__(self):
        return self.gardenID
class Inventory(models.Model):
    """Model for linking the user to their inventory, containing which flowers they have and how many"""
    inventoryID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    blockID = models.ForeignKey('Block', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


    def has_block(self):
        """Checks if the user has the block in their inventory"""
        return self.quantity > 0

    def add_block(self):
        """Increases the block quantity in the inventory"""
        self.quantity += 1
        self.save()

    def remove_block(self, amount=1):
        """Decreases the block quantity in the inventory if possible"""
        if self.quantity >= amount:
            self.quantity -= amount
            self.save()
            return True
        return False


    def __str__(self):
        return self.inventoryID
class Block(models.Model):
    """Model for hte block, containing the name, cost, and value of the block"""
    blockID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    visibleName = models.CharField(max_length=50, default="")
    blockPath = models.FileField(upload_to='blocks/', null=True, blank=True)
    cost = models.IntegerField(default=0)
    value = models.IntegerField(default=0)




