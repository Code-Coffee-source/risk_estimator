
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage_view.as_view(), name='homepage'),
]
