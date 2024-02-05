from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('requests_for_driver/', views.requests_for_driver, name='requests_for_driver_name'),
]
