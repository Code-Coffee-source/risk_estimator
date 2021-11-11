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
