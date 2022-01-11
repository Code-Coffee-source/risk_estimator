
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage_view.as_view(), name='homepage'),
    path('how_to_use', views.instructions_view.as_view(), name='instructions'),
]
