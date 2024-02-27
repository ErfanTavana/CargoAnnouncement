from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [

    path('create_captcha/', views.create_captcha, name='create_captcha_name'),

]
