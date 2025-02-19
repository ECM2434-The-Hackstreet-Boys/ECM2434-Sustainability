import os.path

from django.db import models



def garden_file_path(instance, filename):
    return os.path.join('gardens', f'{instance.userID.username}_{instance.name}.json')
# Create your models here.
class Garden(models.Model):
    gardenID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    file_path = models.FileField(upload_to=garden_file_path, null=True, blank=True)
    rating = models.FloatField(default=0)


    def __str__(self):
        return self.gardenID


class Inventory(models.Model):
    inventoryID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    blockID = models.ForeignKey('block', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return self.inventoryID


class Block(models.Model):
    blockID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    cost = models.IntegerField(default=0)
    value = models.IntegerField(default=0)