from django.db import models

# Create your models here.

# Model for storing the QR codes and respective locations
class QRCodes(models.Model):
    qrID = models.AutoField(primary_key=True)
    location = models.CharField(max_length=512)
    qrCodeLink = models.CharField(max_length=512)

    def __str__(self):
        return self.qrID


# Model for storing the bins and respective qr codes
class Bin(models.Model):
    binID = models.AutoField(primary_key=True)
    location = models.CharField(max_length=512)
    qrCode = models.ForeignKey('QRCodes', on_delete=models.CASCADE)

    def __str__(self):
        return self.binID


# Model for storing types of items that can go into bins and their respective carbon values
class Items(models.Model):
    itemID = models.AutoField(primary_key=True)
    itemName = models.CharField(max_length=512)
    itemDescription = models.CharField(max_length=512)
    itemCarbonValue = models.FloatField()

    def __str__(self):
        return self.itemID
