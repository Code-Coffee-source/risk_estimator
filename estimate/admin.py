from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.LocationInfo)
admin.site.register(models.ActivityPreset)
admin.site.register(models.MaskType)
