from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .models import LocationInfo, ActivityPreset, MaskType, Ventilation, result_formula, ActivityLevels, utilities
from django.urls import reverse_lazy, reverse

from . import forms

import json
import os
import fnmatch

summary_data = {
    "Location":  {
            "value" : None,
            "edit_link" : reverse_lazy('location')

        },

    "Activity":  {
            "value" : None,
            "edit_link" : reverse_lazy('activity')
        },

    "Intensity":  {
            "value" : None,
            "edit_link" : None,
        },

    "Floor Area":  {
            "value": None,
            "edit_link" : None
        },

    "Room Height":  {
            "value": None,
            "edit_link" : None
        },

    "Ventilation":  {
            "value" : None,
            "edit_link" : None
        },

    "Duration":  {
            "value" : None,
            "edit_link" : reverse_lazy('timeAndPeople')
        },

    "Number Of People":  {
            "value" : None,
            "edit_link" : reverse_lazy('timeAndPeople')
        },

    "Mask Percentage":  {
            "value" : None,
            "edit_link" : reverse_lazy('masks')
        },

    "Mask Type": {
            "value" : None,
            "edit_link" : reverse_lazy('masks')

        },

    }

data = {
    "breathingRate" : 1.56,
    "infectivePeople" : 1,
    "decayRate" : 0.62,
    "virusDeposition" : 0.3,
    "breathingRate" :  1.56,
    "fractionImmune" :  0.0,
    "controlMeasures" : 0.0,
}
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
        context['stage_desc'] =  "Choose what region the activity will take place."
        context['stage_number'] = 1

        context['nonEstimateLinks'] = utilities.nonEstimateLinks()

        return context

    def form_valid(self, form):


        location_code = form.cleaned_data.get("location")

        location = LocationInfo.objects.get(Code = location_code)

        data.update({

            "numberOfCases": float(location.Cases),
            "population": float(location.Population),
        })


        utilities.update_summary(summary_data, "Location", location.Region,  reverse_lazy("location"))

        return super().form_valid(form)

    def form_invalid(self, form):
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
        context['stage_desc'] =  "Choose your preferred planned activity during the pandemic:"
        context['stage_number'] = 2

        context['presets'] = ActivityPreset.objects.all()
        context['nonEstimateLinks'] = utilities.nonEstimateLinks()

        return context

    def form_valid(self, form):

        activity = ActivityPreset.objects.get(Code = form.cleaned_data.get("activity"))

        ventilation = Ventilation.objects.get(Activity=activity.id)

        data.update({
            "roomVolume": float(activity.get_room_volume()),
            "Height": float(activity.Room_Height),
            'floorArea': float(activity.Floor_Area),
            "quantaExhalationRate": float(activity.Activity_Level.QuantaExhalationRate),
            "occupantDensity": float(ventilation.Occupant_Density),
            "peopleOutdoorRate": float(ventilation.People_Outdoor_Air_Rate),
            "areaOutdoorRate": float(ventilation.Area_Outdoor_Air_Rate),
        })



        utilities.update_summary(summary_data, "Activity", activity.Name, reverse_lazy("activity"))
        utilities.update_summary(summary_data, "Intensity", activity.Activity_Level.Name, None)
        utilities.update_summary(summary_data, "Floor Area", f"{float(activity.Floor_Area)} meter/s", None)
        utilities.update_summary(summary_data, "Room Height", f"{float(activity.Room_Height)} meter/s", None)

        utilities.update_summary(summary_data, "Ventilation", ventilation.Name, None)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class activity_level_view(FormView):
    template_name = 'activity_level.html'
    form_class = forms.ActivityLevelForm
    success_url = reverse_lazy('room_ventilation')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['activity_levels'] = ActivityLevels.objects.all()

        context['back_link'] = reverse_lazy('activity')
        context['stage_title'] = "Activity Level"
        context['stage_desc'] =  "Click the left or right button (or slide when using mobile) to choose the intensity. The intensity increases from left to right."
        context['stage_number'] = 2.1

        context['nonEstimateLinks'] = utilities.nonEstimateLinks()

        return context

    def form_valid(self, form):


        activity_level = ActivityLevels.objects.get(Code=form.cleaned_data.get("activity_level"))
        activity_sub_level = self.request.POST.get("activity_sub_level")

        intensity_link = reverse_lazy('activity_level')

        if activity_sub_level == "Oral_breathing":
            quantaExhalationRate = float(activity_level.Oral_breathing)

        elif activity_sub_level == "Speaking":
            quantaExhalationRate = float(activity_level.Speaking)

        else:
            quantaExhalationRate = float(activity_level.Loudly_speaking)

        data.update({
            'quantaExhalationRate': quantaExhalationRate
        })




        utilities.update_summary(summary_data, "Activity", "Custom", reverse_lazy("activity"))
        utilities.update_summary(summary_data, "Intensity", f"{activity_level.Name} ({activity_sub_level})", intensity_link)

        return super().form_valid(form)

    def form_invalid(self, form):
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
        context['stage_number'] = 2.2

        context['nonEstimateLinks'] = utilities.nonEstimateLinks()

        return context

    def form_valid(self, form):

        ventilation = Ventilation.objects.get(Code = form.cleaned_data.get("ventilation"))

        ventilation_link =  reverse_lazy('room_ventilation')

        data.update({
            "occupantDensity": float(ventilation.Occupant_Density),
            "peopleOutdoorRate": float(ventilation.People_Outdoor_Air_Rate),
            "areaOutdoorRate": float(ventilation.Area_Outdoor_Air_Rate),
        })



        utilities.update_summary(summary_data, "Ventilation", ventilation.Name, ventilation_link)

        return super().form_valid(form)

    def form_invalid(self, form):
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
        context['stage_number'] = 2.3

        context['nonEstimateLinks'] = utilities.nonEstimateLinks()

        return context

    def form_valid(self, form):

        Length = float(form.cleaned_data.get("length"))
        Width = float(form.cleaned_data.get("width"))
        Height = float(form.cleaned_data.get("height"))

        data.update({
            "roomVolume": float(ActivityPreset.get_custom_room_volume(Length, Width, Height)),
            "Height": Height,
            'floorArea': float(ActivityPreset.get_custom_floor_area(Length, Width)),
        })



        size_link = reverse_lazy('room_size')

        utilities.update_summary(summary_data, "Floor Area", f"{float(Length*Width)} meter/s", size_link)
        utilities.update_summary(summary_data, "Room Height", f"{float(Height)} meter/s", size_link)

        return super().form_valid(form)

    def form_invalid(self, form):
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
        context['stage_number'] = 3


        context['nonEstimateLinks'] = utilities.nonEstimateLinks()

        return context

    def form_valid(self, form):

        t_unit = form.cleaned_data.get("t_unit")
        t_value = form.cleaned_data.get("time")
        people = form.cleaned_data.get("people")

        t_mins = t_value if t_unit == "minutes" else f"{t_value* 60}"
        t_hours = t_value if t_unit == "hours" else f"{t_value / 60}"

        self.request.session['numberOfPeople'] = people


        data.update({
            "eventDuration": t_mins,
            "numberOfPeople": people
        })




        utilities.update_summary(summary_data, "Duration", f"{t_mins} minute(s) ({round(float(t_hours), 3)} hour(s))", reverse_lazy('timeAndPeople'))
        utilities.update_summary(summary_data, "Number Of People", form.cleaned_data.get("people"), reverse_lazy('timeAndPeople'))

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class masks_view(FormView):
    template_name = 'masks.html'
    form_class = forms.masksForm
    success_url = reverse_lazy('summary')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['masks'] = MaskType.objects.all()

        context['back_link'] = reverse_lazy('timeAndPeople')
        context['stage_title'] = "Masks"
        context['stage_desc'] =  "You are almost done!"
        context['stage_number'] = 4


        context['nonEstimateLinks'] = utilities.nonEstimateLinks()

        return context

    def form_valid(self, form):

        maskCode = form.cleaned_data.get("maskType")
        maskType = MaskType.objects.get(Code = maskCode)

        data.update({
            'inhalationMaskEfficiency': float(maskType.inhalationMaskEfficiency),
            'exhalationMaskEfficiency': float(maskType.exhalationMaskEfficiency),
            'peopleWithMasks': self.request.session['numberOfPeople'] * float(form.cleaned_data.get("maskPercent"))
        })





        utilities.update_summary(summary_data, "Mask Percentage", f"{form.cleaned_data.get('maskPercent')}%", reverse_lazy('masks'))
        utilities.update_summary(summary_data, "Mask Type", maskType.Name, reverse_lazy('masks'))

        return super().form_valid(form)

class summary_view(TemplateView):
    template_name = 'summary.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['stage_title'] = "Summary"
        context['stage_desc'] =  "You can check and edit your selections below. Return to this page by clicking the Summary button."
        context['stage_number'] = 5
        context['back_link'] = self.request.META.get('HTTP_REFERER')

        context["summary_data"] = summary_data

        context['nonEstimateLinks'] = utilities.nonEstimateLinks()

        return(context)


class result_view(TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context['stage_title'] = "Results"
        context['stage_desc'] =  "Check the results below"
        context['stage_number'] = 5

        risk_score = result_formula.get_risk_score(result_formula, data["breathingRate"], data["eventDuration"], data["inhalationMaskEfficiency"], data["peopleWithMasks"], data["roomVolume"], data["quantaExhalationRate"], data["exhalationMaskEfficiency"], data["infectivePeople"], data["decayRate"], data["virusDeposition"], data["controlMeasures"], data["occupantDensity"], data["floorArea"], data["peopleOutdoorRate"], data["areaOutdoorRate"], data["numberOfCases"], data["population"], data["numberOfPeople"], data["fractionImmune"])

        risk_obj = result_formula.get_risk_level(result_formula, risk_score)

        context["result_name"] = risk_obj.Name
        context["result_title"] = risk_obj.Name.replace('_', ' ').title()
        context["result_desc"] = risk_obj.Desc
        context["result_image"] = risk_obj.image.url

        context['nonEstimateLinks'] = utilities.nonEstimateLinks()

        return context
