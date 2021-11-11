from django.db import models

# Create your models here.
class LocationInfo(models.Model):

    Region = models.CharField(max_length=225, default="")
    Population = models.IntegerField()
    Cases = models.IntegerField()
    Code = models.CharField(max_length=225, default="")

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations Information"

    def __str__(self):
        return self.Region

class ActivityPreset(models.Model):

    Name = models.CharField(max_length=225, default="")
    Code = models.CharField(max_length=225, default="")

    class Meta:
        verbose_name = "Preset"
        verbose_name_plural = "Activity Presets"

    def __str__(self):
        return self.Name

class MaskType(models.Model):

    Name = models.CharField(max_length=225, default="")
    Code = models.CharField(max_length=225, default="")

    class Meta:
        verbose_name = "Masks"
        verbose_name_plural = "Mask Types"

    def __str__(self):
        return self.Name