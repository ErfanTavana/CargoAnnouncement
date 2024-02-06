from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('delivered_driver_req/', views.delivered_driver_req, name='delivered_driver_req_name'),
    path('sent_driver_req/', views.sent_driver_req, name='sent_driver_req_name'),
]
