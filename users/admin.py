from django.contrib import admin
from .models import Log, Package, UserProfile

admin.site.register(UserProfile)
admin.site.register(Package)
admin.site.register(Log)
