from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('RoadFleet/', views.road_fleet_view, name='road_fleet_view_name'),
    path('ListDriverForCarOwn/',views.driver_list_carrier_owner,name='driver_list_carrier_owner_name'),
    path('driver_list_carrier_owner/', views.driver_list_carrier_owner, name='driver_list_carrier_owner_name'),
    path('CarOwReqDriver/', views.car_ow_req_driver_view, name='car_ow_req_driver_view_name'),
    path('required_carrier_list_view/', views.required_carrier_list_view, name='required_carrier_list_view_name'),

]
