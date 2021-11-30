from django.contrib import admin
from . import models

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    list_display = ('Region', 'Population', 'Cases', 'Code')

admin.site.register(models.LocationInfo, LocationAdmin)

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code', )


admin.site.register(models.ActivityPreset, ActivityAdmin)
admin.site.register(models.MaskType)

class VentilationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code', 'Use_In_Custom')

admin.site.register(models.Ventilation, VentilationAdmin)

class ActivityLevelAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code')

admin.site.register(models.ActivityLevels, ActivityLevelAdmin)
