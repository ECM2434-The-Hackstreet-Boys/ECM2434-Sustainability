from django.db import models

# Create your models here.
class Garden(models.Model):
    gardenID = models.AutoField(primary_key=True)
    userID = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    filePath = models.FilePathField()
    rating = models.FloatField(default=0)


    def __str__(self):
        return self.gardenID


class