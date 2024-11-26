from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_CHOICE = (
        ('M', 'Man'),
        ('W', 'Woman'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    profile_picture = models.ImageField(upload_to='profile_picture', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth = models.DateField(blank=True, null=True)