from django.urls import path
from . import views

urlpatterns = [
    path('location', views.location_view.as_view(), name='location'),

    path('activity', views.activity_presets_view.as_view(), name='activity'),
    path('activity/custom/room_size', views.room_size_view.as_view(), name='room_size'),
    path('activity/custom/room_ventilation', views.room_ventilation_view.as_view(), name='room_ventilation'),
    path('activity/custom/activity_level', views.activity_level_view.as_view(), name='activity_level'),

    path('time_and_people', views.timeAndPeople_view.as_view(), name='timeAndPeople'),

    path('masks', views.masks_view.as_view(), name='masks'),

    path('results', views.result_view.as_view(), name='result')
]