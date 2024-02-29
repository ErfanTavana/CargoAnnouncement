from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('delivered_goods_owner_req/', views.requests_received_carrier_owner,
         name='requests_received_carrier_owner_name'),
]
