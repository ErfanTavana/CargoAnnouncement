from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('requests_received_carrier_owner/', views.requests_received_carrier_owner,
         name='requests_received_carrier_owner_name'),
]
