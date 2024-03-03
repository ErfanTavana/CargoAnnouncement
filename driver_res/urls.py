from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('requests_received_carrier_owner_driver/', views.requests_received_carrier_owner_DRIVER,
         name='requests_received_carrier_owner_DRIVER_name')
]
