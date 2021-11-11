from django.urls import path
from . import views

urlpatterns = [
    path('location', views.location_view.as_view(), name='location'),
    path('activity', views.activity_presets_view.as_view(), name='activity'),
    path('time_and_people', views.timeAndPeople_view.as_view(), name='timeAndPeople'),
    path('masks', views.masks_view.as_view(), name='masks'),
    path('results', views.result_view.as_view(), name='result')
]