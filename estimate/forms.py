from django import forms 
from . import models, widgets

class LocationForm(forms.Form):

    location = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget = forms.TextInput(attrs={
            'id': 'location',})


class PresetsForm(forms.Form):

    activity = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(PresetsForm, self).__init__(*args, **kwargs)
        self.fields['activity'].widget = forms.TextInput(attrs={
            'id': 'activity',})

class VentilationForm(forms.Form):

    ventilation = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(VentilationForm, self).__init__(*args, **kwargs)
        self.fields['ventilation'].widget = forms.TextInput(attrs={
            'id': 'ventilation',})

class SizeForm(forms.Form):

    width = forms.IntegerField()
    length = forms.IntegerField()
    height = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(SizeForm, self).__init__(*args, **kwargs)

        self.fields['width'].widget = forms.NumberInput(attrs={
            'id': 'width',})

        self.fields['length'].widget = forms.NumberInput(attrs={
            'id': 'length',})

        self.fields['height'].widget = forms.NumberInput(attrs={
            'id': 'height',})

class ActivityLevelForm(forms.Form):

    activity_level = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ActivityLevelForm, self).__init__(*args, **kwargs)

        self.fields['activity_level'].widget = forms.NumberInput(attrs={
            'id': 'activity_level',})

class timeAndPeopleForm(forms.Form):

    time = forms.IntegerField()
    t_unit = forms.CharField()
    people = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(timeAndPeopleForm, self).__init__(*args, **kwargs)

        self.fields['t_unit'].widget = forms.TextInput(attrs={
            'id': 'unit',})

        self.fields['time'].widget = forms.NumberInput(attrs={
            'id': 'time',})

        self.fields['people'].widget = forms.NumberInput(attrs={
            'id': 'people',})


class masksForm(forms.Form):

    maskPercent = forms.IntegerField()
    maskType = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(masksForm, self).__init__(*args, **kwargs)

        self.fields['maskPercent'].widget = forms.NumberInput(attrs={
            'id': 'maskPercent',})

        self.fields['maskType'].widget = forms.TextInput(attrs={
            'id': 'maskType',})
