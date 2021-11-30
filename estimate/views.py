from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .models import LocationInfo, ActivityPreset, MaskType, Ventilation, result_formula, ActivityLevels
from django.urls import reverse_lazy, reverse

from . import forms

import json
import os
import fnmatch

# Create your views here.
class location_view(FormView):
    template_name = 'location.html'
    form_class = forms.LocationForm
    success_url = reverse_lazy('activity')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['regions'] = LocationInfo.objects.all()

        context['back_link'] = reverse_lazy('homepage')
        context['stage_title'] = "Activity Location"
        context['stage_desc'] =  "Kindly choose what region the activity will take place."
        return context

    def form_valid(self, form):
        self.request.session["Location"] = form.cleaned_data.get("location")
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        print(form.errors)
        print(form.cleaned_data)
        return super().form_invalid(form)

class activity_presets_view(FormView):
    template_name = 'presets.html'
    form_class = forms.PresetsForm
    success_url = reverse_lazy('timeAndPeople')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['back_link'] = reverse_lazy('location')
        context['stage_title'] = "Activity Planned"
        context['stage_desc'] =  "Kindly choose your preferred plan activity during the pandemic:"

        context['presets'] = ActivityPreset.objects.all()
        return context

    def form_valid(self, form):
        self.request.session["Activity"] = form.cleaned_data.get("activity")
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        print(form.errors)
        print(form.cleaned_data)
        return super().form_invalid(form)

class activity_level_view(FormView):
    template_name = 'activity_level.html'
    form_class = forms.ActivityLevelForm
    success_url = reverse_lazy('room_ventilation')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['back_link'] = reverse_lazy('activity')
        context['stage_title'] = "Activity Level"
        context['stage_desc'] =  "Drag the slider to choose the intensity of the activity. Intensity increases from left to right"

        context['presets'] = ActivityPreset.objects.all()
        return context

    def form_valid(self, form):
        self.request.session["Activity_level"] = form.cleaned_data.get("activity_level")
        print(self.request.session["Activity_level"])
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        print(form.errors)
        print(form.cleaned_data)
        return super().form_invalid(form)

class room_ventilation_view(FormView):
    template_name = 'room_ventilation.html'
    form_class = forms.VentilationForm
    success_url = reverse_lazy('room_size')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['ventilation_presets'] = Ventilation.objects.filter(Use_In_Custom=True)

        context['back_link'] = reverse_lazy('activity_level')
        context['stage_title'] = "Ventilation"
        context['stage_desc'] =  "To calculate your rooms ventilation, choose your activity location category."

        return context

    def form_valid(self, form):
        self.request.session["Ventilation"] = form.cleaned_data.get("ventilation")
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        print(form.errors)
        print(form.cleaned_data)
        return super().form_invalid(form)


class room_size_view(FormView):
    template_name = 'room_size.html'
    form_class = forms.SizeForm
    success_url = reverse_lazy('timeAndPeople')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['ventilation_presets'] = Ventilation.objects.filter(Use_In_Custom=True)

        context['back_link'] = reverse_lazy('room_ventilation')
        context['stage_title'] = "Room Size"

        return context

    def form_valid(self, form):
        self.request.session["Length"] = form.cleaned_data.get("length")
        self.request.session["Width"] = form.cleaned_data.get("width")
        self.request.session["Height"] = form.cleaned_data.get("height")
        self.request.session["Activity"]  = "Custom"
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        print(form.errors)
        print(form.cleaned_data)
        return super().form_invalid(form)

class timeAndPeople_view(FormView):
    template_name = 'timeAndPeople.html'
    form_class = forms.timeAndPeopleForm
    success_url = reverse_lazy('masks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['back_link'] = reverse_lazy('activity')
        context['stage_title'] = "Time and People"
        context['stage_desc'] =  "Kindly estimate how long the activity will take and how many people are involved:"

        return context

    def form_valid(self, form):
        self.request.session["Time"] = form.cleaned_data.get("time")
        self.request.session["People"] = form.cleaned_data.get("people")
        self.request.session["T_unit"] = form.cleaned_data.get("t_unit")

        for key, value in self.request.session.items():
            print('{} => {}'.format(key, value))

        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        print(form.errors)
        print(form.cleaned_data)
        return super().form_invalid(form)

class masks_view(FormView):
    template_name = 'masks.html'
    form_class = forms.masksForm
    success_url = reverse_lazy('result')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['masks'] = MaskType.objects.all()

        context['back_link'] = reverse_lazy('timeAndPeople')
        context['stage_title'] = "Masks"
        context['stage_desc'] =  "You are almost done!"

        return context

    def form_valid(self, form):
        self.request.session["maskType"] = form.cleaned_data.get("maskType")
        self.request.session["maskPercent"] = form.cleaned_data.get("maskPercent")

        for key, value in self.request.session.items():
            print('{} => {}'.format(key, value))

        return super().form_valid(form)

class result_view(TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["result"] = 1

        try:
            location = LocationInfo.objects.get(Code=self.request.session["Location"])
            mask = MaskType.objects.get(Code=self.request.session["maskType"])
            
            data_values = {
            "location": location.Region,
            "location_data": {
                "numberOfCases": location.Cases,
                "population": location.Population
            },
            "eventDuration": self.request.session["Time"],
            "t_unit":  self.request.session["T_unit"],
            "numberOfPeople": self.request.session["People"],
            "peopleWithMasks": self.request.session["maskPercent"] / 100,
            "masks_information": {
                "mask_type": mask.Name,
                "inhalationMaskEfficiency": mask.inhalationMaskEfficiency,
                "exhalationMaskEfficiency": mask.exhalationMaskEfficiency
            },
            "infectivePeople": 1,
            "decayRate": 0.62,
            "virusDeposition": 0.3,
            "breathingRate": 1.56,
            "fractionImmune": 0,
        }
        except(KeyError):
            pass


        try:

            if self.request.session["Activity"] != "Custom":

                activity = ActivityPreset.objects.get(Code=self.request.session["Activity"])
                ventilation = Ventilation.objects.get(Activity=activity.id)

                data_values["activity"] = activity.Name

                data_values["room_dimensions"] = {
                    "floorArea": activity.Floor_Area,
                    "roomHeight": activity.Room_Height,
                    "roomVolume": activity.get_room_volume(),
                }

                data_values["ventilation"] = {
                    "ventilation": ventilation.Name,
                    "occupantDensity": ventilation.Occupant_Density,
                    "peopleOutdoorRate": ventilation.People_Outdoor_Air_Rate,
                    "areaOutdoorRate": ventilation.Area_Outdoor_Air_Rate
                }

                data_values["activityLevel"] = activity.Activity_Level.Name
                data_values["quantaExhalationRate"] = activity.Activity_Level.QuantaExhalationRate

            else:

                ventilation = Ventilation.objects.get(Code=self.request.session["Ventilation"])

                data_values["activity"] = "Custom"

                data_values["ventilation"] = {
                    "ventilation": ventilation.Name,
                    "occupantDensity": ventilation.Occupant_Density,
                    "peopleOutdoorRate": ventilation.People_Outdoor_Air_Rate,
                    "areaOutdoorRate": ventilation.Area_Outdoor_Air_Rate
                }

                data_values["room_dimensions"] = {
                    "roomLength": self.request.session["Length"],
                    "roomWidth": self.request.session["Width"],
                    "roomHeight": self.request.session["Height"],
                    "floorArea": ActivityPreset.get_custom_floor_area(self.request.session["Length"], self.request.session["Width"]),
                    "roomVolume": ActivityPreset.get_custom_room_volume(self.request.session["Length"], self.request.session["Width"], self.request.session["Height"])
                }

                data_values["activity_level"] = ActivityLevels.objects.get(Name=self.request.session["Activity_level"]).Name
                data_values["quantaExhalationRate"] = ActivityLevels.objects.get(Name=self.request.session["Activity_level"]).QuantaExhalationRate

        except(KeyError):
            pass

        result = result_formula.mainFunction(result_formula, data_values["breathingRate"], data_values["eventDuration"], data_values["masks_information"]["inhalationMaskEfficiency"],
                                            data_values["peopleWithMasks"], data_values["room_dimensions"]["roomVolume"], data_values["quantaExhalationRate"],
                                            data_values["masks_information"]["exhalationMaskEfficiency"], data_values["infectivePeople"], data_values["decayRate"],
                                            data_values["virusDeposition"], data_values["ventilation"]["occupantDensity"], data_values["room_dimensions"]["floorArea"],
                                            data_values["ventilation"]["peopleOutdoorRate"], data_values["ventilation"]["areaOutdoorRate"],
                                            data_values["location_data"]["numberOfCases"], data_values["location_data"]["population"],
                                            data_values["numberOfPeople"], data_values["fractionImmune"])

        data_values["result"] = result

        print(result)

        return context


