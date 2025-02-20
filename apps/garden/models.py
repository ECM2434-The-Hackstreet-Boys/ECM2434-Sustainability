from django.db import models

# Create your models here.
class Garden(models.Model):
    gardenID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    filePath = models.FilePathField()
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