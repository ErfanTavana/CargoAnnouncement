from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('rail_cargo_confirmation/', views.rail_cargo_confirmation, name='rail_cargo_confirmation_name'),

]
