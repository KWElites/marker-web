from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default = 'profilePics/defaultPP.jpg', upload_to = 'profilePics')
    name = models.CharField(max_length=30)

class Packages(models.Model):
    uId = models.ForeignKey(User,on_delete=models.RESTRICT)
    packageName = models.CharField(max_length=20)
    packageDesc = models.CharField(max_length=512)
    packageThumbnail = models.ImageField(default='package/thumbnails/defaultTN.png',upload_to='package/thumbnails')
    #packageItems = models.FileField(upload_to='package/packages',default='')


class Logs(models.Model):
    pId = models.ForeignKey(Packages,on_delete=models.RESTRICT)
    uId = models.ForeignKey(User,on_delete=models.RESTRICT)
    logAction = models.CharField(max_length=8)
    logDesc = models.CharField(max_length=512)
    logErrorCode = models.SmallIntegerField()
    logActionStatus = models.BooleanField()