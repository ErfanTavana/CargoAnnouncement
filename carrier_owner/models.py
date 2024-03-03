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


# کلاس RoadFleet از Base_Model ارث‌بری کرده است و اطلاعات مرتبط با حمل‌ونقل در سیستم را نمایش می‌دهد.

class RoadFleet(Base_Model):
    # اطلاعات مرتبط با کاربران
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    carrier_owner = models.ForeignKey(CarrierOwner, on_delete=models.CASCADE, verbose_name='صاحب حمل کننده', blank=True,
                                      null=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='required_carriers', null=True, blank=True)

    # اطلاعات نوع مالکیت و اتاق حمل‌ونقل
    ownerType = models.CharField(max_length=100, verbose_name="نوع مالکیت", default="",
                                 choices=(
                                     ("مالکیتی", "مالکیتی"),
                                     ("شرکتی", "شرکتی"),
                                 ))
    roomType = models.CharField(max_length=100, verbose_name="نوع اتاق", default="",
                                choices=(
                                    ("چادری", "چادری"),
                                    ("روباز", "روباز"),
                                    ("یخچالی", "یخچالی"),
                                    ("کمپرسی", "کمپرسی"),
                                    ("مسقف", "مسقف"),
                                    ("کفی", "کفی"),
                                    ("بفل دار", "بقل دار"),
                                ))

    # اطلاعات نوع وسیله حمل‌ونقل
    vehichleType = models.CharField(max_length=100, verbose_name="نوع وسیله حمل کننده", default="",
                                    choices=(
                                        ("تریلی", "تریلی"),
                                        ("جفت", "جفت"),
                                        ("تک", "تک"),
                                        ("خاور", "خاور"),
                                        ("وانت و نیسان", "وانت ونیسان"),
                                        ("خاور", "خاور"),

                                    ))
    # vehichleTypeOthers = models.CharField(max_length=100, verbose_name="سایر", default="")

    # اطلاعات نوع ماشین باربری نیمه سنگین
    # # semiHeavyVehichle = models.CharField(max_length=20, verbose_name="ماشین باربری نیمه سنگین", default="",
    #                                      choices=(
    #                                          ("کامیون", "کامیون"),
    #                                          ("خاور", "خاور"),
    #                                          ("هیوندا", "هیوندا"),
    #                                          ("ماشین باربری ایسوزو", "ماشین باربری ایسوزو"),
    #                                          ("کامیونت", "کامیونت"),
    #                                          ("سایر", "سایر"),
    #
    #                                      ))
    # semiHeavyVehichleOthers = models.CharField(max_length=100, verbose_name="سایر", default="")

    # اطلاعات نوع ماشین باربری سنگین
    # HeavyVehichle = models.CharField(max_length=20, verbose_name="ماشین باربری سنگین", default="",
    #                                  choices=(
    #                                      ("تریلی", "تریلی"),
    #                                      ("ترانزیت", "ترانزیت"),
    #                                      ("ده تن", "ده تن"),
    #                                      ("کفی", "کفی"),
    #                                      ("ترانزیت یخچالی", "ترانزیت یخچالی"),
    #                                      ("بیست تن", "بیست تن"),
    #                                      ("چادری سه محور", "چادری سه محور"),
    #                                      ("کمپرسی", "کمپرسی"),
    #                                      ("تریلی تانکر فاو", "تریلی تانکر فاو"),
    #                                      ("سایر", "سایر"),
    #
    #                                  ))
    # heavy_vehicle_others = models.CharField(max_length=100, verbose_name="سایر", default="")

    # اطلاعات شماره پلاک‌ها
    plaque_one_num_check = models.BooleanField(verbose_name="شماره پلاک واحد(تک پلاک)", default="")
    plaque_one_num = models.CharField(max_length=9, verbose_name="ثبت شماره پلاک واحد(تک پلاک)", default="")
    plaque_puller_num_check = models.BooleanField(verbose_name="شماره پلاک کشنده", default="")
    plaque_puller_num = models.CharField(max_length=9, verbose_name="ثبت شماره پلاک کشنده", default="")
    plaque_carriage_num_check = models.BooleanField(verbose_name="شماره پلاک گاری", default="")
    plaque_carriage_num = models.CharField(max_length=9, verbose_name="ثبت شماره پلاک گاری", default="")
    plaque_container_num_check = models.BooleanField(verbose_name="شماره پلاک کانتینر", default="")
    plaque_container_num = models.CharField(max_length=9, verbose_name="ثبت شماره پلاک کانتینر", default="")

    # اطلاعات آپلود تصاویر
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

    # اطلاعات مربوط به مدارک شناسایی
    code_id = models.CharField(max_length=12, verbose_name="کد ملی  / شماره پاسپورت مالک", default="")
    owner_document = models.ImageField(max_length=800, verbose_name="آپلود کارت ملی / پاسپورت مالک", default="",
                                       upload_to="", blank=True, null=True)
    international_docs = models.ImageField(max_length=800, verbose_name="آپلود مدارک مجوز حمل بین المللی در صورت وجود",
                                           default="", upload_to="", blank=True, null=True)
    international_docs_bool = models.BooleanField(default=False,
                                                  verbose_name="آپلود مدارک مجوز حمل بین المللی در صورت وجود")

    # نوع حمل و نقل داخلی یا بین المللی
    CARRIER_CHOICES = (
        ('حمل و نقل داخلی', 'حمل و نقل داخلی'),
        ('حمل و نقل بین المللی', 'حمل و نقل بین المللی'),
        ('داخلی و بین المللی', 'داخلی و بین المللی'),

    )
    carrier_type = models.CharField(max_length=40, default='حمل و نقل بین المللی', choices=CARRIER_CHOICES,
                                    verbose_name="نوع حمل و نقل")

    class Meta:
        verbose_name = "حمل کننده های مربوط به صاحب حمل کننده"
        verbose_name_plural = "حمل کننده های مربوط به صاحاب حمل کنندهها "

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        # تنظیم مقادیر فیلد‌های boolean بر اساس وجود تصاویر
        if self.vehicle_card is not None:
            self.vehicle_card_bool = True
        if self.vehicle_property_doc is not None:
            self.vehicle_property_doc_bool = True
        if self.vehicle_advocate is not None:
            self.vehicle_advocate_bool = True
        if self.international_docs is not None:
            self.international_docs_bool = True
        super().save(*args, **kwargs)


# CHOICES برای نتایج ممکن برای درخواست همکاری
REQUEST_RESULT_CHOICES = [
    ('در انتظار پاسخ', 'در انتظار پاسخ'),
    ('تایید شده', 'تایید شده'),
    ('رد شده', 'رد شده'),
    ('لغو شده', 'لغو شده'),
]
