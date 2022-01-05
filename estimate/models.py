from django.db import models
import numpy as np
import json
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

    def get_disease_prevalence(self):
        population = self.Population
        cases = self.Cases

        return cases / population

class ActivityLevels(models.Model):

    Name = models.CharField(max_length=225, default="")
    Desc = models.CharField(max_length=225, default="")
    QuantaExhalationRate = models.FloatField(max_length=225, default=0)
    Code = models.CharField(max_length=225, default="")
    Image = models.FileField(blank=True, null=True, upload_to="ActivityLevls")
    Oral_breathing = models.FloatField(max_length=225, default=0)
    Speaking = models.FloatField(max_length=225, default=0)
    Loudly_speaking = models.FloatField(max_length=225, default=0)

    class Meta:
        verbose_name = "Activity Level"
        verbose_name_plural = "Activity Levels"

    def __str__(self):
        return self.Name

class ActivityPreset(models.Model):

    Name = models.CharField(max_length=225, default="")
    Floor_Area = models.FloatField(default=0)
    Room_Height = models.FloatField(default=0)
    Code = models.CharField(max_length=225, default="")
    Activity_Level = models.ForeignKey(ActivityLevels, on_delete=models.CASCADE, null=True, blank=True)
    Image = models.FileField(blank=True, null=True, upload_to="ActivityPresets")

    class Meta:
        verbose_name = "Preset"
        verbose_name_plural = "Activity Presets"

    def __str__(self):
        return self.Name

    def get_custom_floor_area(length, width):
        return length * width

    def get_room_volume(self):
        return self.Floor_Area * self.Room_Height

    def get_custom_room_volume(length, width, height):
        return length * width * height

class MaskType(models.Model):

    Name = models.CharField(max_length=225, default="")
    inhalationMaskEfficiency = models.FloatField(default=0)
    exhalationMaskEfficiency = models.FloatField(default=0)
    Code = models.CharField(max_length=225, default="")
    image = models.FileField(blank=True, null=True, upload_to="masks")


    class Meta:
        verbose_name = "Masks"
        verbose_name_plural = "Mask Types"

    def __str__(self):
        return self.Name

class Ventilation(models.Model):

    Name = models.CharField(max_length=225, default="")
    Activity=models.OneToOneField(ActivityPreset, on_delete=models.CASCADE, null=True, blank=True)
    People_Outdoor_Air_Rate = models.FloatField(default=0)
    Area_Outdoor_Air_Rate = models.FloatField(default=0)
    Occupant_Density = models.FloatField(default=0)
    Use_In_Custom = models.BooleanField(default=False)
    Code = models.CharField(max_length=225, default="")
    image = models.FileField(blank=True, null=True, upload_to="VentilationCustoms")

    class Meta:
        verbose_name = "Ventilation Values"
        verbose_name_plural = "Ventilation Rates"

    def __str__(self):
        return self.Name

class result_formula(models.Model):

    Name = models.CharField(max_length=300, default="")
    upper_value = models.FloatField(default=0)
    lower_value = models.FloatField(default=0)
    Desc = models.CharField(max_length=225, default="")
    image = models.FileField(blank=True, null=True, upload_to="Results")

    class Meta:
        verbose_name = "Result Type Settings"
        verbose_name_plural = "Results"

    def get_risk_level(self, risk_score):

        queryset = self._meta.model.objects.all()

        risk_level = None
        while risk_level == None:
            for object in queryset:

                risk_level = object if (risk_score >= object.lower_value) & (risk_score < object.upper_value) else None

                if risk_level != None:
                    break

        return risk_level

    def __str__(self):
        return self.Name

    #Formula 1
    def probInfectionFunction(quantaInhaled, diseasePrevalenceFunction, peopleSusceptible):
        return 1 - (1 - diseasePrevalenceFunction * (1 - np.exp(-quantaInhaled))) ** peopleSusceptible

    #Formula 2
    def quantaInhaledFunction(meanQuantaConcentration, breathingRate, eventDuration, inhalationMaskEfficiency, peopleWithMasks):
        return float(meanQuantaConcentration) * float(breathingRate) * float(eventDuration) * (1 - float(inhalationMaskEfficiency) * float(peopleWithMasks))

    #Formula 4
    def emissionRateFunction(quantaExhalationRate, exhalationMaskEfficiency, peopleWithMasks, infectivePeople):
        return quantaExhalationRate * (1 - exhalationMaskEfficiency * peopleWithMasks) * infectivePeople

    #Formula 3
    def meanQuantaConcentrationFunction(emissionRate, lossRate, roomVolume, eventDuration):
        return float(float(emissionRate) / float(lossRate) / float(roomVolume) * (1 - (1 / float(lossRate) / float(eventDuration)) * (1 - np.exp(float(-lossRate) * float(eventDuration)))))

    #Formula 5
    def lossRateFunction(outsideVentilation, decayRate, virusDeposition, controlMeasures):
        return outsideVentilation + decayRate + virusDeposition + controlMeasures

    #Formula 7
    def ventilationRateFunction(occupantDensity, floorArea, peopleOutdoorRate, areaOutdoorRate):
        return (occupantDensity * (floorArea/100) * peopleOutdoorRate + floorArea * areaOutdoorRate)

    #Formula 6
    def outsideVentilationFunction(ventilationRate, roomVolume):
        return ventilationRate * 3600 * (0.001 / roomVolume)

    #Formula 8
    def diseasePrevalenceFunction(numberOfCases, population):
        return numberOfCases / population

    #Formula 9
    def peopleSusceptibleFunction(numberOfPeople, infectivePeople, fractionImmune):
        return (numberOfPeople - infectivePeople) * (1 - fractionImmune)

    def get_risk_score(self, breathingRate, eventDuration, inhalationMaskEfficiency, peopleWithMasks, roomVolume, quantaExhalationRate, exhalationMaskEfficiency,
                      infectivePeople, decayRate, virusDeposition, controlMeasures, occupantDensity, floorArea,
                     peopleOutdoorRate, areaOutdoorRate, numberOfCases, population, numberOfPeople, fractionImmune):

        data_dict = {key:val for key, val in locals().items() if key != 'self'}


        result = self.probInfectionFunction(self.quantaInhaledFunction(self.meanQuantaConcentrationFunction(self.emissionRateFunction(quantaExhalationRate, exhalationMaskEfficiency, peopleWithMasks, infectivePeople), self.lossRateFunction(self.outsideVentilationFunction(self.ventilationRateFunction(occupantDensity, floorArea, peopleOutdoorRate, areaOutdoorRate), roomVolume), decayRate, virusDeposition, controlMeasures), roomVolume, eventDuration), breathingRate, eventDuration, inhalationMaskEfficiency, peopleWithMasks), self.diseasePrevalenceFunction(numberOfCases, population), self.peopleSusceptibleFunction(numberOfPeople, infectivePeople, fractionImmune))

        data_dict["result"] = result

        return result
