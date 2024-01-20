from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('InnerCargo/', views.inner_cargo_view, name='inner_cargo_view_name'),
]