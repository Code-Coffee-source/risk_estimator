from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .models import LocationInfo, ActivityPreset, MaskType
from django.urls import reverse_lazy, reverse

from . import forms

# Create your views here.
class location_view(FormView):
    template_name = 'location.html'
    form_class = forms.LocationForm
    success_url = reverse_lazy('activity')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['regions'] = LocationInfo.objects.all()
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

class timeAndPeople_view(FormView):
    template_name = 'timeAndPeople.html'
    form_class = forms.timeAndPeopleForm
    success_url = reverse_lazy('masks')

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

        try:
            context['location'] = LocationInfo.objects.get(Code=self.request.session["Location"])
        except(KeyError):
            pass

        try:
            context['activity'] = ActivityPreset.objects.get(Code=self.request.session["Activity"])
        except(KeyError):
            pass

        try:
            context['time'] = Code=self.request.session["Time"]
        except(KeyError):
            pass

        try:
            context['t_unit'] = self.request.session["T_unit"]
        except(KeyError):
            pass

        try:
            context['people'] = self.request.session["People"]
        except(KeyError):
            pass

        try:
            context['maskType'] = MaskType.objects.get(Code=self.request.session["maskType"])
        except(KeyError):
            pass

        try:
            context['maskPercent'] = self.request.session["maskPercent"]
        except(KeyError):
            pass

        return context


