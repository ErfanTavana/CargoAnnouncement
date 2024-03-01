from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('cargo_wagon_coordination/', views.cargo_wagon_coordination, name='cargo_wagon_coordination_name'),
    path('sent_collaboration_request_to_railCargo/', views.sent_collaboration_request_to_railCargo,
         name='sent_collaboration_request_to_railCargo_name'),


]
