from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('carrier_owner_list_for_driver/', views.carrier_owner_list_for_driver,
         name='carrier_owner_list_for_driver_name'),
    path('driver_req_carrier_owner/', views.driver_req_carrier_owner, name='driver_req_carrier_owner_name'),
]
