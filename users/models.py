from django.db import models
from django.contrib import admin


class Account(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    salt = models.CharField(max_length=50)