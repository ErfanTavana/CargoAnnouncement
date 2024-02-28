from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('InnerCargo/', views.inner_cargo_view, name='inner_cargo_view_name'),
    path('InternationalCargo/', views.international_cargo_view, name='international_cargo_view'),
    path('RequiredCarrier/', views.required_carrier_view, name='required_carrier'),
    path('wagon_cargo_view/', views.wagon_cargo_view, name='wagon_cargo_view_name'),
    path('required_wagon_view/', views.required_wagon_view, name='required_wagon_view_name'),

]
