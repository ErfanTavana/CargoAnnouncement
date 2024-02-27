from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('InnerCargo/', views.inner_cargo_view, name='inner_cargo_view_name'),
    path('InternationalCargo/', views.international_cargo_view, name='international_cargo_view'),
    path('RequiredCarrier/', views.required_carrier_view, name='required_carrier'),
    path('road_fleet_list_goods_owner/', views.road_fleet_list_goods_owner, name='road_fleet_list_goods_owner_name'),
    path('goods_owner_req_car_ow/', views.goods_owner_req_car_ow, name='goods_owner_req_car_ow_name'),
    path('list_cargo/', views.list_cargo, name='list_cargolist_cargo_name'),
    path('wagon_cargo_view/', views.wagon_cargo_view, name='wagon_cargo_view_name'),
    path('required_wagon_view/', views.required_wagon_view, name='required_wagon_view_name'),

]
