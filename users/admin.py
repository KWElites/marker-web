from django.contrib import admin
from .models import Log, Package, UserProfile, Store

admin.site.register(UserProfile)
admin.site.register(Store)
admin.site.register(Package)
admin.site.register(Log)
