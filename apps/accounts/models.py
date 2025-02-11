from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# Custom user model extending AbstractUser
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username