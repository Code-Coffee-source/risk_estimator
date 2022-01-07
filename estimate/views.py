from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .models import LocationInfo, ActivityPreset, MaskType, Ventilation, result_formula, ActivityLevels
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


def import_data_values(file_name):

    with open(file_name) as f:
        data = json.load(f)

    return(data)

def get_data_values(self):

    try:
        data = {key: value for (key, value) in self.request.session.items()}

        return data
    except KeyError as e:
        print(e.message)
        pass

def update_summary(item, value, edit_link):
    try:
        summary_data[item]["value"] = value
        summary_data[item]["edit_link"] = edit_link
    except KeyError:
        pass

def generate_risk_values(self):
    data["location"] = self.request.session["Location"]
    data["activity"] = "custom" if self.request.session["Activity"] == "Custom" else self.request.session["Activity"]

    data["maskType"] = self.request.session["maskType"]


    data["inhalationMaskEfficiency"] = float(MaskType.objects.get(Name = data["maskType"]).inhalationMaskEfficiency)
    data["exhalationMaskEfficiency"] = float(MaskType.objects.get(Name = data["maskType"]).exhalationMaskEfficiency)

    data["numberOfCases"] = float(LocationInfo.objects.get(Region = data["location"]).Cases)
    data["population"] = float(LocationInfo.objects.get(Region = data["location"]).Population)

    data["numberOfPeople"] = float(self.request.session["People"])
    data["eventDuration"] = float(self.request.session["Time"])
    data["peopleWithMasks"] = float(self.request.session["People"] * (self.request.session["maskPercent"]/100))

    if data["activity"] != "custom":
        data["Height"] = float(ActivityPreset.objects.get(Name = data['activity']).Room_Height)
        data["roomVolume"] = float(ActivityPreset.objects.get(Name = data['activity']).get_room_volume())
        data["floorArea"] = float(ActivityPreset.objects.get(Name = data['activity']).Floor_Area)
        data["quantaExhalationRate"] = float(ActivityPreset.objects.get(Name = data['activity']).Activity_Level.QuantaExhalationRate)

        data["ventilation"] = Ventilation.objects.get(Activity=ActivityPreset.objects.get(Name = data['activity']).id).Name

    else:
        data["Length"] = self.request.session["Length"]
        data["Width"] = self.request.session["Width"]
        data["Height"] = self.request.session["Length"]

        data["ventilation"] = self.request.session["Ventilation"]

        data["roomVolume"] = float(ActivityPreset.get_custom_room_volume(data["Length"], data["Width"], data["Height"]))
        data["floorArea"] = float(ActivityPreset.get_custom_floor_area(data["Length"], data["Width"]))

        if self.request.session["Activity_sub_level"] == "Oral_breathing":
            data["quantaExhalationRate"] = float(ActivityLevels.objects.get(Name=self.request.session["Activity_level"]).Oral_breathing)

        elif self.request.session["Activity_sub_level"] == "Speaking":
            data["quantaExhalationRate"] = float(ActivityLevels.objects.get(Name=self.request.session["Activity_level"]).Speaking)

        else:
            data["quantaExhalationRate"] = float(ActivityLevels.objects.get(Name=self.request.session["Activity_level"]).Loudly_speaking)


    data["occupantDensity"] = float(Ventilation.objects.get(Name = data["ventilation"]).Occupant_Density)
    data["peopleOutdoorRate"] = float(Ventilation.objects.get(Name = data["ventilation"]).People_Outdoor_Air_Rate)
    data["areaOutdoorRate"] = float(Ventilation.objects.get(Name = data["ventilation"]).Area_Outdoor_Air_Rate)


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

        context['nonEstimateLinks'] = [reverse_lazy('homepage'), ]

        return context

    def form_valid(self, form):


        location_code = form.cleaned_data.get("location")
        location = LocationInfo.objects.get(Code = location_code)
        self.request.session["Location"] = location.Region

        update_summary("Location", location.Region,  reverse_lazy("location"))

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
        return context

    def form_valid(self, form):

        activity = ActivityPreset.objects.get(Code = form.cleaned_data.get("activity"))

        self.request.session["Activity"] = activity.Name

        intensity_link = None
        size_link = None
        ventilation_link = None


        update_summary("Activity", activity.Name, reverse_lazy("activity"))
        update_summary("Intensity", activity.Activity_Level.Name, intensity_link)
        update_summary("Floor Area", f"{float(activity.Floor_Area)} meter/s", size_link)
        update_summary("Room Height", f"{float(activity.Room_Height)} meter/s", size_link)

        update_summary("Ventilation", Ventilation.objects.get(Activity= activity.id).Name, ventilation_link)
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

        return context

    def form_valid(self, form):


        activity_level = ActivityLevels.objects.get(Code=form.cleaned_data.get("activity_level"))
        activity_sub_level = self.request.POST.get("activity_sub_level")

        self.request.session["Activity_level"] = activity_level
        self.request.session["Activity_sub_level"] = activity_sub_level

        self.request.session["Activity"] = "Custom"

        intensity_link =  None if self.request.session["Activity"] != "Custom" else reverse_lazy('activity_level')
        update_summary("Activity", "Custom", reverse_lazy("activity"))
        update_summary("Intensity", f"{activity_level.Name} ({activity_sub_level})", intensity_link)

        return super().form_valid(form)

    def form_invalid(self, form):
        print(self.request.POST)
        print(form.errors)
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

        return context

    def form_valid(self, form):

        ventilation = Ventilation.objects.get(Code = form.cleaned_data.get("ventilation"))

        self.request.session["Ventilation"] = ventilation.Name

        ventilation_link =  None if self.request.session["Activity"] != "Custom" else reverse_lazy('room_ventilation')
        update_summary("Ventilation", ventilation.Name, ventilation_link)

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

        context['data_values'] = get_data_values(self)

        return context

    def form_valid(self, form):

        Length = form.cleaned_data.get("length")
        Width = form.cleaned_data.get("width")
        Height = form.cleaned_data.get("height")

        self.request.session["Length"] = Length
        self.request.session["Width"] = Width
        self.request.session["Height"] = Height

        size_link = None if self.request.session["Activity"] != "Custom" else reverse_lazy('room_size')

        update_summary("Floor Area", f"{float(Length*Width)} meter/s", size_link)
        update_summary("Room Height", f"{float(Height)} meter/s", size_link)

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

        context['data_values'] = get_data_values(self)
        return context

    def form_valid(self, form):

        t_unit = form.cleaned_data.get("t_unit")
        t_value = form.cleaned_data.get("time")
        people = form.cleaned_data.get("people")

        time = t_value if t_unit == "minutes" else f"{t_value* 60}"

        self.request.session["Time"] = time
        self.request.session["People"] = people

        update_summary("Duration", f"{t_value} minute/s ({round(float(t_value/60), 3)} hour/s)", reverse_lazy('timeAndPeople'))
        update_summary("Number Of People", people, reverse_lazy('timeAndPeople'))

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
        context['data_values'] = get_data_values(self)

        return context

    def form_valid(self, form):

        maskCode = form.cleaned_data.get("maskType")
        maskName = MaskType.objects.get(Code = maskCode).Name

        self.request.session["maskType"] = maskName
        self.request.session["maskPercent"] = form.cleaned_data.get("maskPercent")

        update_summary("Mask Percentage", f"{form.cleaned_data.get('maskPercent')}%", reverse_lazy('masks'))
        update_summary("Mask Type", maskName, reverse_lazy('masks'))

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

        return(context)


class result_view(TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        generate_risk_values(self)

        context['stage_title'] = "Results"
        context['stage_desc'] =  "Check the results below"
        context['stage_number'] = 5

        risk_score = result_formula.get_risk_score(result_formula, data["breathingRate"], data["eventDuration"], data["inhalationMaskEfficiency"], data["peopleWithMasks"], data["roomVolume"], data["quantaExhalationRate"], data["exhalationMaskEfficiency"], data["infectivePeople"], data["decayRate"], data["virusDeposition"], data["controlMeasures"], data["occupantDensity"], data["floorArea"], data["peopleOutdoorRate"], data["areaOutdoorRate"], data["numberOfCases"], data["population"], data["numberOfPeople"], data["fractionImmune"])

        risk_obj = result_formula.get_risk_level(result_formula, risk_score)
        context["result"] = risk_obj


        return context
