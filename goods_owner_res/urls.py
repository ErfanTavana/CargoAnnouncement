from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('delivered_goods_owner_req/', views.delivered_goods_owner_req, name='delivered_goods_owner_req_name'),
    path('sent_goods_owner_req/', views.sent_goods_owner_req, name='sent_goods_owner_req_name'),

]
