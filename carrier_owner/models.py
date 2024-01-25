# Import necessary modules and packages
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random
from rest_framework.authtoken.models import Token
from accounts.models import GoodsOwner, CarrierOwner, Driver
from django.db import models
import datetime
from django.contrib.auth.models import User
from datetime import datetime, timezone
from django.utils import timezone
# from cachetools import TTLCache
from datetime import datetime, timedelta
from goods_owner.models import Base_Model


class RoadFleet(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    carrier_owner = models.ForeignKey(CarrierOwner, on_delete=models.CASCADE, verbose_name='صاحب حمل کننده')

    ownerType = models.CharField(max_length=100, verbose_name="نوع مالکیت", default="",
                                 choices=(
                                     ("مالکیتی", "مالکیتی"),
                                     ("شرکتی", "شرکتی"),))

    roomType = models.CharField(max_length=100, verbose_name="نوع اتاق", default="",
                                choices=(
                                    ("چادری", "چادری"),
                                    ("روباز", "روباز"),
                                    ("یخچالی", "یخچالی"),))

    vehichleType = models.CharField(max_length=100, verbose_name="نوع وسیله حمل کننده", default="",
                                    choices=(
                                        ("ماشین باربری کوچک و سبک", "ماشین باربری کوچک و سبک"),
                                        ("ماشین باربری نیمه سنگین", "ماشین باربری نیمه سنگین"),
                                        ("ماشین حمل بار سنگین", "ماشین حمل بار سنگین"),
                                    ))

    # Semi-Heavy
    semiHeavyVehichle = models.CharField(max_length=20, verbose_name="ماشین باربری نیمه سنگین", default="",
                                         choices=(
                                             ("کامیون", "کامیون"),
                                             ("خاور", "خاور"),
                                             ("هیوندا", "هیوندا"),
                                             ("ماشین باربری ایسوزو", "ماشین باربری ایسوزو"),
                                             ("کامیونت", "کامیونت"),
                                         ))
    semiHeavyVehichleOthers = models.CharField(max_length=100, verbose_name="سایر", default="")

    # Heavy
    HeavyVehichle = models.CharField(max_length=20, verbose_name="ماشین باربری سنگین", default="",
                                     choices=(
                                         ("تریلی", "تریلی"),
                                         ("ترانزیت", "ترانزیت"),
                                         ("ده تن", "ده تن"),
                                         ("کفی", "کفی"),
                                         ("ترانزیت یخچالی", "ترانزیت یخچالی"),
                                         ("بیست تن", "بیست تن"),
                                         ("چادری سه محور", "چادری سه محور"),
                                         ("کمپرسی", "کمپرسی"),
                                         ("تریلی تانکر فاو", "تریلی تانکر فاو"),
                                     ))
    heavy_vehicle_others = models.CharField(max_length=100, verbose_name="سایر", default="")

    plaque_one_num_check = models.BooleanField(verbose_name="شماره پلاک واحد(تک پلاک)", default="")
    plaque_one_num = models.CharField(max_length=9, verbose_name="ثبت شماره پلاک واحد(تک پلاک)", default="")

    plaque_puller_num_check = models.BooleanField(verbose_name="شماره پلاک کشنده", default="")
    plaque_puller_num = models.CharField(max_length=9, verbose_name="ثبت شماره پلاک کشنده", default="")

    plaque_carriage_num_check = models.BooleanField(verbose_name="شماره پلاک گاری", default="")
    plaque_carriage_num = models.CharField(max_length=9, verbose_name="ثبت شماره پلاک گاری", default="")

    plaque_container_num_check = models.BooleanField(verbose_name="شماره پلاک کانتینر", default="")
    plaque_container_num = models.CharField(max_length=9, verbose_name="ثبت شماره پلاک کانتینر", default="")

    vehicle_card = models.ImageField(max_length=800, verbose_name="آپلود کارت ماشین", default="", upload_to="")
    vehicle_property_doc = models.ImageField(max_length=800, verbose_name="آپلود برگه سبز ماشین", default="",
                                             upload_to="")
    vehicle_advocate_date = models.DateTimeField(verbose_name="تاریخ اعتبار بیمه نامه ماشین",
                                                 default=timezone.now)
    vehicle_advocate = models.ImageField(max_length=800, verbose_name="آپلود بیمه نامه ماشین", default="", upload_to="")

    code_id = models.CharField(max_length=12, verbose_name="کد ملی  / شماره پاسپورت مالک", default="")
    owner_document = models.ImageField(max_length=800, verbose_name="آپلود کارت ملی / پاسپورت مالک", default="",
                                       upload_to="")

    international_docs = models.ImageField(max_length=800, verbose_name="آپلود مدارک مجوز حمل بین المللی در صورت وجود",
                                           default="", upload_to="")
    CARRIER_CHOICES = (
        ('حمل و نقل داخلی', 'حمل و نقل داخلی'),
        ('حمل و نقل بین المللی', 'حمل و نقل بین المللی'),
    )
    carrier_type = models.CharField(max_length=30, default='حمل و نقل بین المللی',choices=CARRIER_CHOICES, verbose_name="نوع حمل و نقل")

    class Meta:
        verbose_name = "حمل کننده های مربوط به صاحب حمل کننده"
        verbose_name_plural = "حمل کننده های مربوط به صاحاب حمل کنندهها "

    def __str__(self):
        return self.ownerType
