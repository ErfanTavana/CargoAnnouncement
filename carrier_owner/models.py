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
from goods_owner.models import Base_Model, RequiredCarrier


class RoadFleet(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    carrier_owner = models.ForeignKey(CarrierOwner, on_delete=models.CASCADE, verbose_name='صاحب حمل کننده')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='required_carriers', null=True, blank=True)
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

    vehicle_card = models.ImageField(max_length=800, verbose_name="آپلود کارت ماشین", default="", upload_to="",
                                     blank=True, null=True)
    vehicle_card_bool = models.BooleanField(default=False, verbose_name="آپلود کارت ماشین")
    vehicle_property_doc = models.ImageField(max_length=800, verbose_name="آپلود برگه سبز ماشین", default="",
                                             upload_to="", blank=True, null=True)
    vehicle_property_doc_bool = models.BooleanField(default=False, verbose_name="آپلود برگه سبز ماشین")

    vehicle_advocate_date = models.DateTimeField(verbose_name="تاریخ اعتبار بیمه نامه ماشین",
                                                 default=timezone.now)
    vehicle_advocate = models.ImageField(max_length=800, verbose_name="آپلود بیمه نامه ماشین", default="", upload_to="",
                                         blank=True, null=True)
    vehicle_advocate_bool = models.BooleanField(default=False, verbose_name="آپلود بیمه نامه ماشین")

    code_id = models.CharField(max_length=12, verbose_name="کد ملی  / شماره پاسپورت مالک", default="")
    owner_document = models.ImageField(max_length=800, verbose_name="آپلود کارت ملی / پاسپورت مالک", default="",
                                       upload_to="", blank=True, null=True)

    international_docs = models.ImageField(max_length=800, verbose_name="آپلود مدارک مجوز حمل بین المللی در صورت وجود",
                                           default="", upload_to="", blank=True, null=True)
    international_docs_bool = models.BooleanField(default=False,
                                                  verbose_name="آپلود مدارک مجوز حمل بین المللی در صورت وجود")
    CARRIER_CHOICES = (
        ('حمل و نقل داخلی', 'حمل و نقل داخلی'),
        ('حمل و نقل بین المللی', 'حمل و نقل بین المللی'),
    )
    carrier_type = models.CharField(max_length=30, default='حمل و نقل بین المللی', choices=CARRIER_CHOICES,
                                    verbose_name="نوع حمل و نقل")

    class Meta:
        verbose_name = "حمل کننده های مربوط به صاحب حمل کننده"
        verbose_name_plural = "حمل کننده های مربوط به صاحاب حمل کنندهها "

    def __str__(self):
        return self.ownerType

    def save(self, *args, **kwargs):
        if self.vehicle_card != None:
            self.vehicle_card_bool = True
        if self.vehicle_property_doc != None:
            self.vehicle_property_doc_bool = True
        if self.vehicle_advocate != None:
            self.vehicle_advocate_bool = True
        if self.international_docs != None:
            self.international_docs_bool = True
        super().save(*args, **kwargs)


REQUEST_RESULT_CHOICES = [
    ('در انتظار پاسخ', 'در انتظار پاسخ'),
    ('تایید شده', 'تایید شده'),
    ('رد شده', 'رد شده'),
    ('لغو شده', 'لغو شده'),
]


# درخواست همکاری صاحب حمل کننده از راننده
# CarrierOwnerReqquestDriver
class CarOwReqDriver(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    # ForeignKey به مدل GoodsOwner برای ارتباط با صاحب حمل کننده
    carrier_owner = models.ForeignKey(CarrierOwner, on_delete=models.CASCADE, verbose_name='صاحب حمل کننده')

    # ForeignKey به مدل CarrierOwner برای ارتباط با حمل کننده
    carrier = models.ForeignKey(RoadFleet, on_delete=models.CASCADE, verbose_name='حمل کننده')

    # ForeignKey به مدل Driver برای ارتباط با راننده
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='راننده')

    # گزینه‌های نوع همکاری به عنوان یک Select field
    COLLABORATION_TYPES = [
        ('همکاری دائم (تمام وقت)', 'همکاری دائم (تمام وقت)'),
        ('همکاری موقت (پاره وقت)', 'همکاری موقت (پاره وقت)'),
    ]
    collaboration_type = models.CharField(max_length=40, choices=COLLABORATION_TYPES, verbose_name='نوع همکاری')

    # مبدا مسیر
    origin = models.CharField(max_length=255, verbose_name='مبدا')

    # مقصد مسیر
    destination = models.CharField(max_length=255, verbose_name='مقصد')

    # قیمت پیشنهادی
    proposed_price = models.FloatField(default=0.0, verbose_name='قیمت پیشنهادی')
    request_result = models.CharField(max_length=30, choices=REQUEST_RESULT_CHOICES, verbose_name='نتیجه درخواست')

    def __str__(self):
        return f'{self.carrier_owner} - {self.carrier} - {self.driver} - {self.collaboration_type}'

    class Meta:
        verbose_name = "درخواست همکاری صاحب حمل کننده از راننده"
        verbose_name_plural = "درخواست‌های همکاری صاحب حمل کننده از راننده"


class CarOwReqGoodsOwner(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    carrier_owner = models.ForeignKey(CarrierOwner, on_delete=models.CASCADE, verbose_name='صاحب حمل کننده')
    road_fleet = models.ForeignKey(RoadFleet, on_delete=models.CASCADE, related_name='car_owners',
                                   verbose_name='حمل کننده')

    goods_owner = models.ForeignKey(GoodsOwner, on_delete=models.CASCADE, verbose_name='صاحب بار')
    required_carrier = models.ForeignKey(RequiredCarrier, on_delete=models.CASCADE, verbose_name='درخواست صاحب بار')
    # قیمت پیشنهادی
    proposed_price = models.FloatField(default=0.0, verbose_name='قیمت پیشنهادی')
    request_result = models.CharField(max_length=30, choices=REQUEST_RESULT_CHOICES, verbose_name='نتیجه درخواست')

    class Meta:
        verbose_name = "درخواست همکاری صاحب حمل کننده از صاحب بار"
        verbose_name_plural = "درخواست‌های همکاری صاحب حمل کننده از صاحب بار"
