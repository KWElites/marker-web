from django.contrib import admin
from .models import Logs, Packages, UserProfile

admin.site.register(UserProfile)
admin.site.register(Packages)
admin.site.register(Logs)
