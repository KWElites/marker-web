from django.contrib import admin
from .models import UserProfile
from .models import Packages

admin.site.register(UserProfile)
admin.site.register(Packages)