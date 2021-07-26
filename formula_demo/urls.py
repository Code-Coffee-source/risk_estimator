
from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_area, name='formula_demo')
]
