# This is the urls.py file responsible for handling authentication-related views.

from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for sending a verification code
    path('Send_verification_code/', views.Send_verification_code, name='send_verification_code'),

    # URL pattern for user registration
    path('register/', views.register, name='register'),

    # URL pattern for user login
    path('login/', views.login, name='login'),

    # URL pattern for user logout
    path('logout/', views.logout, name='logout'),

    # URL pattern for handling forget password functionality
    path('forget_password/', views.forget_password, name='forget_password'),

    path('profile_view/', views.profile_view, name='profile_view'),

    path('set_password/', views.set_password, name='set_password'),

]
