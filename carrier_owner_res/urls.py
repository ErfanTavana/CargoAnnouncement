from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('sent_carrier_owner_req/', views.sent_carrier_owner_req, name='sent_carrier_owner_req_name'),
    path('delivered_carrier_owner_req/', views.delivered_carrier_owner_req, name='delivered_carrier_owner_req_name')

]
