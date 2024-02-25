from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('wagon_details_view/', views.wagon_details_view, name='wagon_details_view_name'),


]
