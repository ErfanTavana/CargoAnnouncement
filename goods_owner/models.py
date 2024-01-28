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

# Function to generate a random complex ID
def generate_complex_id():
    id_length = 8  # Length of the generated complex ID
    characters = string.ascii_letters + string.digits  # Set of characters (letters and digits) to choose from
    complex_id = ''.join(
        random.choice(characters) for _ in range(id_length))  # Generate the complex ID using random characters
    return complex_id  # Return the generated complex ID


# Abstract base class for common fields among different models
class Base_Model(models.Model):
    id = models.CharField(primary_key=True, default=generate_complex_id, max_length=10, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ ایجاد')
    deleted_at = models.DateTimeField(default=None, null=True, blank=True, verbose_name='تاریخ حذف')
    is_ok = models.BooleanField(default=False, verbose_name='آیا تایید شده است؟')
    is_changeable = models.BooleanField(default=True, verbose_name='قابل تغییر است ؟')
    is_deletable = models.BooleanField(default=True, verbose_name='قابل حذف است ؟')


    class Meta:
        abstract = True  # Indicates that this class is an abstract class and should not create a table in the database

    def soft_delete(self):
        """
        تابع سافت‌دیلیت برای تنظیم تاریخ و زمان حذف به لحظه فراخوانی تابع
        """
        if self.is_deletable == True:
            self.deleted_at = timezone.now()
            self.is_ok = False  # شاید نیاز به تغییر این فیلد نیز باشد
            self.is_changeable = False
            self.save()


class CommonCargo(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    goods_owner = models.ForeignKey(GoodsOwner, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='پروفایل صاحاب بار')
    # Common Fields
    length = models.IntegerField(verbose_name="طول", default=0, blank=True, null=True)

    width = models.IntegerField(verbose_name="عرض", default=0, blank=True, null=True)
    height = models.IntegerField(verbose_name="ارتفاع", default=0, blank=True, null=True)
    cargoType = models.CharField(max_length=800, verbose_name="عنوان محموله", default="", blank=True, null=True)
    pkgType = models.CharField(max_length=20, verbose_name='نوع بسته بندی', choices=(
        ("کیسه", "کیسه"),
        ("فله", "فله"),
        ("پالت", "پالت"),
        ("جامبو", "جامبو"),
        ("کانتینر", "کانتینر"),
        ("بندی", "بندی"),
        ("رول", "رول"),
        ("سواری", "سواری"),
        ("جعبه", "جعبه"),
        ("کالای خاص", "کالای خاص"),
        ("غیر پالیتیزه", "غیر پالیتیزه"),
        ("غیرمعمول", "غیرمعمول"),
    ), blank=True, null=True)
    description = models.TextField(max_length=5000, verbose_name="توضیحات", default="", blank=True, null=True)
    specialWidgets = models.CharField(max_length=100, verbose_name='ویژگی های خاص', choices=(
        ("روباری", "روباری"),
        ("نیاز به بارنامه ندارد", "نیاز به بارنامه ندارد"),
        ("بارنامه خودم میگیرم", "بارنامه خودم میگیرم"),
    ), blank=True, null=True)
    storageBillNum = models.CharField(max_length=20, verbose_name="شماره قبض انبار", default="", blank=True, null=True)
    storagePrice = models.TextField(max_length=9999, verbose_name="هزینه انبارداری", default="", blank=True, null=True)
    loadigPrice = models.TextField(max_length=9999, verbose_name="هزینه بارگیری", default="", blank=True, null=True)
    basculPrice = models.TextField(max_length=9999, verbose_name="هزینه باسکول", default="", blank=True, null=True)
    specialDesc = models.TextField(max_length=9999, verbose_name="توضیحات خاص", default="", blank=True, null=True)
    sendersName = models.CharField(max_length=100, verbose_name="نام فرستنده", default="", blank=True, null=True)
    sendersFamName = models.CharField(max_length=100, verbose_name="نام خانوادگی فرستنده", default="", blank=True,
                                      null=True)
    senderMobileNum = models.CharField(max_length=12, verbose_name="شماره تلفن / موبایل فرستنده", default="",
                                       blank=True, null=True)
    dischargeTimeDate = models.DateTimeField(max_length=200, verbose_name="تاریخ و ساعت تحویل بار در مقصد",
                                             default=timezone.now, blank=True, null=True)
    duratio_ndischargeTime = models.DurationField(max_length=200, verbose_name="مدت زمان تخلیه بار در مقصد",
                                                  default=timezone.timedelta(hours=0, minutes=0, seconds=0), blank=True,
                                                  null=True)

    # Comment: Unique fields for InnerCargo
    country = models.CharField(max_length=20, verbose_name="کشور مبدا", choices=(
        ("ایران", "ایران"),
        ("روسیه", "روسیه"),
        ("قزاقستان", "قزاقستان"),
        ("ازبکستان", "ازبکستان"),
        ("قرقیزستان", "قرقیزستان"),
        ("تاجیکستان", "تاجیکستان"),
        ("7افغانستان", "افغانستان"),
        ("ارمنستان", "ارمنستان"),
    ), blank=True, null=True)
    state = models.CharField(max_length=20, verbose_name="استان مبدا", blank=True, null=True)
    city = models.CharField(max_length=20, verbose_name="شهر / منطقه / محدوده مبدا", blank=True, null=True)
    street = models.CharField(max_length=50, verbose_name="خیابان مبدا", blank=True, null=True)
    address = models.CharField(max_length=100, verbose_name="آدرس دقیق مبدا", blank=True, null=True)
    customName = models.CharField(max_length=100, verbose_name="نام کمرگ مبدا", default="", blank=True, null=True)

    class Meta:
        verbose_name = 'اعلام بار اطلاعات  مشترک'
        abstract = True


class InnerCargo(CommonCargo):
    deliveryTimeDate = models.DateTimeField(
        max_length=200,
        verbose_name="تاریخ و ساعت تحویل بار در مبدا",
        default=timezone.now,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'اعلام بار داخلی'
        verbose_name_plural = 'اعلام بار های  داخلی'


class InternationalCargo(CommonCargo):
    senderCountry = models.CharField(max_length=20, verbose_name="کشور مبدا", choices=(
        ("ایران", "ایران"),
        ("روسیه", "روسیه"),
        ("قزاقستان", "قزاقستان"),
        ("ازبکستان", "ازبکستان"),
        ("قرقیزستان", "قرقیزستان"),
        ("تاجیکستان", "تاجیکستان"),
        ("7افغانستان", "افغانستان"),
        ("ارمنستان", "ارمنستان"),
    ), blank=True, null=True)
    senderState = models.CharField(max_length=20, verbose_name="استان مبدا", blank=True, null=True)
    senderCity = models.CharField(max_length=20, verbose_name="شهر / منطقه / محدوده مبدا", blank=True, null=True)
    senderStreet = models.CharField(max_length=50, verbose_name="خیابان", blank=True, null=True)
    senderAddress = models.CharField(max_length=100, verbose_name="آدرس دقیق مبدا", blank=True, null=True)
    deliveryTimeDate = models.DateTimeField(max_length=200, verbose_name="تاریخ و ساعت تحویل بار در مبدا",
                                            default=timezone.now, blank=True, null=True)
    dischargeTimeDate = models.DateTimeField(max_length=200, verbose_name="تاریخ و ساعت تحویل بار در مقصد",
                                             default=timezone.now, blank=True, null=True)
    dischargeTime = models.DurationField(max_length=200, verbose_name="مدت زمان تخلیه بار در مقصد",
                                         default=timezone.timedelta(hours=0, minutes=0, seconds=0), blank=True,
                                         null=True)
    # customName = models.CharField(max_length=100, verbose_name="نام کمرگ مبدا", default="", blank=True, null=True)
    customNameEnd = models.CharField(max_length=100, verbose_name="نام کمرگ مقصد", default="", blank=True, null=True)

    class Meta:
        verbose_name = 'اعلام بار خارجی'
        verbose_name_plural = 'اعلام بار های خارجی'


class RequiredCarrier(Base_Model):
    relinquished = models.BooleanField(default=False, verbose_name="واگذار شده؟")
    CARGO_TYPE_CHOICES = [
        ('اعلام بار داخلی', 'اعلام بار داخلی'),
        ('اعلام بار خارجی', 'اعلام بار خارجی'),
        ('اعلام بار ریلی', 'اعلام بار ریلی'),
    ]
    cargo_type = models.CharField(max_length=20, choices=CARGO_TYPE_CHOICES, verbose_name='نوع بار')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)

    inner_cargo = models.ForeignKey(InnerCargo, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='اعلام بار داخلی', related_name='inner_cargo_carriers')
    international_cargo = models.ForeignKey(InternationalCargo, blank=True, null=True, on_delete=models.CASCADE,
                                            verbose_name='اعلام بار خارجی', related_name='international_cargo_carriers')

    cargo_weight = models.FloatField(max_length=100, verbose_name="وزن خالص محموله")
    counter = models.PositiveIntegerField(verbose_name="تعداد حمل کننده مورد نیاز")
    room_type = models.CharField(max_length=100, verbose_name="نوع اتاق مناسب", choices=(
        ("چادری", "چادری"),
        ("روباز", "روباز"),
        ("یخچالی", "یخچالی"),
    ))
    vehichle_type = models.CharField(max_length=100, verbose_name="نوع وسیله حمل کننده مورد نیاز", choices=(
        ("ماشین باربری کوچک و سبک", "ماشین باربری کوچک و سبک"),
        ("ماشین باربری نیمه سنگین", "ماشین باربری نیمه سنگین"),
        ("ماشین حمل بار سنگین", "ماشین حمل بار سنگین"),
    ))

    semi_heavy_vehichle = models.CharField(max_length=20, verbose_name="ماشین باربری نیمه سنگین ", choices=(
        ("کامیون", "کامیون"),
        ("خاور", "خاور"),
        ("هیوندا", "هیوندا"),
        ("ماشین باربری ایسوزو", "ماشین باربری ایسوزو"),
        ("کامیونت", "کامیونت"),
    ))
    semi_heavy_vehichle_others = models.CharField(max_length=100, verbose_name="سایر", default="")

    heavy_vehichle = models.CharField(max_length=20, verbose_name="ماشین باربری سنگین", choices=(
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
    heavy_vehichle_others = models.CharField(max_length=100, verbose_name="سایر", default="",blank=True,null=True)

    special_widget_carrier = models.TextField(max_length=9999, verbose_name="ویژگی های خاص حمل کننده مورد نیاز",blank=True,null=True)
    carrier_price = models.IntegerField(default=0,verbose_name="قیمت تقریبی حمل",blank=True,null=True)

    # فیلدهای مختص به حمل بین المللی
    cargo_price = models.PositiveIntegerField(default=0,verbose_name="ارزش بار هر حمل کننده / خودرو",blank=True,null=True)

    class Meta:
        verbose_name = 'حمل‌کننده مورد نیاز اعلام بار'
        verbose_name_plural = 'حمل‌کننده‌های مورد نیاز اعلام بار'


# # Model for the request of transportation from a driver
# class CarrierReqToDriver(Base_Model):
#     driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_carrier_requests',
#                                verbose_name='راننده')
#     carrier = models.ForeignKey(RoadFleet, on_delete=models.CASCADE, verbose_name='حمل‌کننده')
#     carrier_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_requests',
#                                       verbose_name='صاحب حمل‌کننده')
#     collaboration_type = models.CharField(max_length=20, default="full_time", verbose_name='نوع همکاری',
#                                           choices=(
#                                               ('full_time', 'تمام وقت'),
#                                               ('part_time', 'پاره وقت/بار موردی'),
#                                           ))
#     proposed_price = models.FloatField(default=0, verbose_name='قیمت پیشنهادی')
#     origin = models.CharField(max_length=100, blank=True, null=True, verbose_name='مبدا بار ')
#
#     # Additional features based on the type of collaboration
#     destination = models.CharField(max_length=100, verbose_name='مقصد بار ', blank=True, null=True)
#     arrival_date_at_origin = models.DateField(verbose_name='تاریخ حضور در مبدا', blank=True, null=True)
#
#     class Meta:
#         verbose_name = 'درخواست صاحب حمل‌کننده از راننده'
#         verbose_name_plural = "درخواست های صاحب حمل‌کننده از راننده"
#
#
# # Model for the request of a carrier owner to a driver
# class CarrierReqToGoodsOwner(Base_Model):
#     CARGO_TYPE_CHOICES = [
#         ('inner_cargo', 'اعلام بار داخلی'),
#         ('international_cargo', 'اعلام بار خارجی'),
#         ('rail_cargo', 'اعلام بار ریلی'),
#     ]
#
#     cargo_type = models.CharField(max_length=20, default='inner_cargo', choices=CARGO_TYPE_CHOICES,
#                                   verbose_name='نوع همکاری')
#     carrier_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goods_owner_requests',
#                                       verbose_name='صاحب حمل‌کننده')
#     carrier = models.ForeignKey(RoadFleet, on_delete=models.CASCADE, verbose_name='حمل‌کننده')
#     goods_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goods_owner_carrier_requests',
#                                     verbose_name='صاحب بار')
#     inner_cargo = models.ForeignKey(InnerCargo, on_delete=models.CASCADE, blank=True, null=True,
#                                     verbose_name='بار داخلی')
#     international_cargo = models.ForeignKey(InternationalCargo, on_delete=models.CASCADE, blank=True, null=True,
#                                             verbose_name='بار خارجی')
#
#     price = models.FloatField(default=0, verbose_name='قیمت پیشنهادی', )
#
#     class Meta:
#         verbose_name = 'درخواست صاحب حمل‌کننده به  صاحب بار'
#         verbose_name_plural = "درخواست های صاحب حمل‌کننده به صاحب بار"
