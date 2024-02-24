from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('increase_wallet_balance/', views.increase_wallet_balance, name='increase_wallet_balance_name'),
]
