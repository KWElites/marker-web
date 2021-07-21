from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default = 'profilePics/defaultPP.jpg', upload_to = 'profilePics')
    name = models.CharField(max_length=30)

class Store(models.Model):
    uId = models.ForeignKey(User,on_delete=models.RESTRICT)
    storeName = models.CharField(max_length=20, verbose_name="Store Name")

class Package(models.Model):
    uId = models.ForeignKey(User,on_delete=models.RESTRICT)
    sId = models.ForeignKey(Store,on_delete=models.RESTRICT, default=0)    
    packageName = models.CharField(max_length=20, verbose_name="Package Name")
    packageDesc = models.CharField(max_length=512, verbose_name="Package Description")
    packageThumbnail = models.ImageField(default='package/thumbnails/defaultTN.png', upload_to='package/thumbnails', verbose_name="Package Thumbnail")
    packageItems = models.FileField(upload_to='package/packages', default='', verbose_name="Package Zip File")
    packageImages = models.CharField(max_length=200, default='')
    # packageQRCode = models.CharField(max_length=200,default='')


class Log(models.Model):
    pId = models.ForeignKey(Package, on_delete=models.RESTRICT)
    uId = models.ForeignKey(User, on_delete=models.RESTRICT)
    logAction = models.CharField(max_length=8)
    logDesc = models.CharField(max_length=512)
    logErrorCode = models.SmallIntegerField()
    logActionStatus = models.BooleanField()