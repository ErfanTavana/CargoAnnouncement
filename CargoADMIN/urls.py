from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('drivers_list/', views.drivers_list, name='drivers_list_name'),
]
