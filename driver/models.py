# Import necessary modules and packages
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random
from rest_framework.authtoken.models import Token
# from wag.models import RoadFleet
from accounts.models import GoodsOwner, CarrierOwner, Driver
from carrier_owner.models import Base_Model, RoadFleet

# CHOICES برای نتایج ممکن برای درخواست همکاری
REQUEST_RESULT_CHOICES = [
    ('در انتظار پاسخ', 'در انتظار پاسخ'),
    ('تایید شده', 'تایید شده'),
    ('رد شده', 'رد شده'),
    ('لغو شده', 'لغو شده'),
]

CARGO_TYPE_CHOICES = [
    ('اعلام بار داخلی', 'اعلام بار داخلی'),
    ('اعلام بار خارجی', 'اعلام بار خارجی'),
    ('اعلام بار ریلی', 'اعلام بار ریلی'),
]


class DriverReqCarrierOwner(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='required_carriers', null=True,
                               blank=True, verbose_name='راننده')

    carrier_owner = models.ForeignKey(CarrierOwner,on_delete=models.CASCADE,verbose_name='صاحب حمل کننده', blank=True,
                                      null=True)
    cargo_type = models.CharField(max_length=20, default='اعلام بار داخلی', choices=CARGO_TYPE_CHOICES,
                                  verbose_name='نوع همکاری')

    # قیمت پیشنهادی
    proposed_price = models.FloatField(default=0.0, verbose_name='قیمت پیشنهادی')

    # نتیجه درخواست
    request_result = models.CharField(max_length=30, choices=REQUEST_RESULT_CHOICES, verbose_name='نتیجه درخواست')

    # زمان لغو درخواست
    cancellation_time = models.DateTimeField(null=True, blank=True, verbose_name='زمان لغو درخواست')

    # مبدا و مقصد
    source = models.CharField(max_length=255, blank=True, null=True, verbose_name='مبدا')
    destination = models.CharField(max_length=255, blank=True, null=True, verbose_name='مقصد')

    class Meta:
        verbose_name = "درخواست همکاری راننده از صاحب حمل کننده"
        verbose_name_plural = "درخواست های  همکاری راننده از صاحب حمل کننده"
