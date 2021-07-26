from django.views.generic import ListView, FormView, DetailView, UpdateView, CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.shortcuts import render
from .forms import AreaForm
from .models import calculation


def calculate_area(request):
    if request.method == 'POST':
        form = AreaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            length = data.get('length')
            width = data.get('width')

            return render(request,'results.html', {
                'result':calculation.calculate_area(length=data.get('length'),width=data.get('width'))
                })
    else:
        form = AreaForm()
        return render(request,'formula_demo.html', {'form':form})