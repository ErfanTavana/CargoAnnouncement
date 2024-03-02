# این فایل urls.py مسئول مدیریت آدرس‌های اینترنتی مربوط به ویوهای مربوط به احراز هویت است.

from django.urls import path
from . import views

urlpatterns = [
    path('info_cargoFleet_Coordination/', views.info_cargoFleet_Coordination, name='info_cargoFleet_Coordination_name'),
    path('sent_collaboration_request_to_goods_owner/', views.sent_collaboration_request_to_goods_owner,
         name='sent_collaboration_request_to_goods_owner_name'),

    ################################################################
    # ارسال درخواست همکاری به راننده

]
