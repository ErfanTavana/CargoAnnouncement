from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('sent_driver_req/', views.sent_driver_req, name='sent_driver_req_name'),
]
