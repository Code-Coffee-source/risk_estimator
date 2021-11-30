from django.db import models
import numpy as np

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
    QuantaExhalationRate = models.FloatField(max_length=225, default="")
    Code = models.CharField(max_length=225, default="")

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
    image = models.ImageField(blank=True, null=True, upload_to="ActivityPresets")

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
    image = models.ImageField(blank=True, null=True, upload_to="masks")


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
    image = models.ImageField(blank=True, null=True, upload_to="VentilationCustoms")

    class Meta:
        verbose_name = "Ventilation Values"
        verbose_name_plural = "Ventilation Rates"

    def __str__(self):
        return self.Name

class result_formula:

    #Formula 1
    def probInfectionFunction(quantaInhaled, diseasePrevalenceFunction, peopleSusceptible):
        probability_of_infection = 1 - (1 - diseasePrevalenceFunction * (1 - np.exp(-quantaInhaled))) ** peopleSusceptible
        print(f"probability of infection => {probability_of_infection}" )
        return probability_of_infection

    #Formula 2
    def quantaInhaledFunction(meanQuantaConcentration, breathingRate, eventDuration, inhalationMaskEfficiency, peopleWithMasks):
        return round(meanQuantaConcentration * breathingRate * eventDuration * (1 - inhalationMaskEfficiency * peopleWithMasks), 2)

    #Formula 4
    def emissionRateFunction(quantaExhalationRate, exhalationMaskEfficiency, peopleWithMasks, infectivePeople):
        return quantaExhalationRate * (1 - exhalationMaskEfficiency * peopleWithMasks) * infectivePeople

    #Formula 3
    def meanQuantaConcentrationFunction(emissionRate, lossRate, roomVolume, eventDuration):
        return round(emissionRate / lossRate / roomVolume * (1 - (1 / lossRate / eventDuration) * (1 - np.exp(-lossRate * eventDuration))), 2)

    #Formula 5
    def lossRateFunction(outsideVentilation, decayRate, virusDeposition):
        return outsideVentilation + decayRate + virusDeposition

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

    def mainFunction(self, breathingRate, eventDuration, inhalationMaskEfficiency, peopleWithMasks, roomVolume, quantaExhalationRate, exhalationMaskEfficiency,
                    infectivePeople, decayRate, virusDeposition, occupantDensity, floorArea,
                    peopleOutdoorRate, areaOutdoorRate, numberOfCases, population, numberOfPeople, fractionImmune):

        return self.probInfectionFunction(
                self.quantaInhaledFunction(self.meanQuantaConcentrationFunction(self.emissionRateFunction(quantaExhalationRate, exhalationMaskEfficiency, peopleWithMasks, infectivePeople),
                self.lossRateFunction(self.outsideVentilationFunction(self.ventilationRateFunction(occupantDensity, floorArea, peopleOutdoorRate, areaOutdoorRate), roomVolume), decayRate, virusDeposition), roomVolume, eventDuration), breathingRate, eventDuration, inhalationMaskEfficiency, peopleWithMasks),
                self.diseasePrevalenceFunction(numberOfCases, population), self.peopleSusceptibleFunction(numberOfPeople, infectivePeople, fractionImmune))

