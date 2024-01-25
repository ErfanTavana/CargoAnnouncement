from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('RoadFleet/', views.road_fleet_view, name='road_fleet_view_name'),

]
