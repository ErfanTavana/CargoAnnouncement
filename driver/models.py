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
from carrier_owner.models import Base_Model


# # Define a meaningful related name for the DriverReqToCarrier model
# class DriverReqToCarrier(Base_Model):
#     CARGO_TYPE_CHOICES = [
#         ('inner_cargo', 'اعلام بار داخلی'),
#         ('international_cargo', 'اعلام بار خارجی'),
#         ('rail_cargo', 'اعلام بار ریلی'),
#     ]
#
#     cargo_type = models.CharField(max_length=20, default='inner_cargo', choices=CARGO_TYPE_CHOICES,
#                                   verbose_name='نوع همکاری')
#     driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_requests_to_carriers',
#                                verbose_name='راننده')
#     carrier = models.ForeignKey(CarrierOwner, on_delete=models.CASCADE, verbose_name='صاحب حمل کننده')
#     price = models.FloatField(default=0, verbose_name='قیمت پیشنهادی', )
#     origin = models.CharField(max_length=100, blank=True, null=True, verbose_name='مبدا راننده')
