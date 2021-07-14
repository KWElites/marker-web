from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default = 'profilePics/defaultPP.jpg', upload_to = 'profilePics')
    company_name = models.CharField(max_length=30,default="Company")

class Packages(models.Model):
    UID = models.ForeignKey(User,on_delete=models.RESTRICT)
    PName = models.CharField(max_length=20)
    PDescription = models.CharField(max_length=512)
    PThumbnail = models.ImageField(default='package/Thumbnails/defaultTN.png')

class Logs(models.Model):
    PID = models.ForeignKey(Packages,on_delete=models.RESTRICT)
    UID = models.ForeignKey(User,on_delete=models.RESTRICT)
    LAction = models.CharField(max_length=8)
    LDescription = models.CharField(max_length=512)
    LErrorCode = models.SmallIntegerField()
    LActionStatus = models.BooleanField()