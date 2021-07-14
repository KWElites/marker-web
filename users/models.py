from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default = 'profilePics/defaultPP.jpg', upload_to = 'profilePics')
    name = models.CharField(max_length=20, unique=True, default=None)