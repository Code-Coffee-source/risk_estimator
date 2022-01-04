from django.contrib import admin
from django import forms
from django_svg_image_form_field import SvgAndImageFormField
from . import models

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    list_display = ('Region', 'Population', 'Cases', 'Code')

admin.site.register(models.LocationInfo, LocationAdmin)

class ActivityAdminForm(forms.ModelForm):
    class Meta:
        model = models.ActivityPreset
        exclude = []
        field_class = {
        'Image': SvgAndImageFormField
        }

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code', )
    form = ActivityAdminForm


admin.site.register(models.ActivityPreset, ActivityAdmin)

class MaskTypeAdminForm(forms.ModelForm):
    class Meta:
        model = models.ActivityPreset
        exclude = []
        field_class = {
            'image': SvgAndImageFormField
        }

class MaskTypeAdmin(admin.ModelAdmin):
    form = MaskTypeAdminForm

admin.site.register(models.MaskType, MaskTypeAdmin)

class VentilationAdminForm(forms.ModelForm):
    class Meta:
        model = models.Ventilation
        exclude = []
        field_class = {
            'image': SvgAndImageFormField
        }

class VentilationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code', 'Use_In_Custom')
    form = VentilationAdminForm

admin.site.register(models.Ventilation, VentilationAdmin)

class ActivityLevelAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Code')

admin.site.register(models.ActivityLevels, ActivityLevelAdmin)

admin.site.register(models.result_formula)
