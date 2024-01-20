# Import necessary modules and packages
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random
from rest_framework.authtoken.models import Token
# from Wagon.wag.models import RoadFleet , InnerCargo , InternationalCargo
# from wag.models import *
from accounts.models import GoodsOwner, CarrierOwner, Driver
from django.db import models
import datetime
from django.contrib.auth.models import User
from datetime import datetime, timezone
from django.utils import timezone


# Function to generate a random complex ID
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    deleted_at = models.DateTimeField(default=None, null=True, blank=True, verbose_name='تاریخ حذف')
    is_ok = models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')
    is_changeable = models.BooleanField(default=True, verbose_name='قابل تغییر است ؟')

    class Meta:
        abstract = True  # Indicates that this class is an abstract class and should not create a table in the database

    def soft_delete(self):
        """
        تابع سافت‌دیلیت برای تنظیم تاریخ و زمان حذف به لحظه فراخوانی تابع
        """
        self.deleted_at = timezone.now()
        self.is_ok = False  # شاید نیاز به تغییر این فیلد نیز باشد
        self.save()


class CommonCargo(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    goods_owner = models.ForeignKey(GoodsOwner, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='پروفایل صاحاب بار')
    # Common Fields
    length = models.IntegerField(verbose_name="طول", default="", blank=True, null=True)
    width = models.IntegerField(verbose_name="عرض", default="", blank=True, null=True)
    height = models.IntegerField(verbose_name="ارتفاع", default="", blank=True, null=True)
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
    ))
    description = models.TextField(max_length=5000, verbose_name="توضیحات", default="", blank=True, null=True)
    specialWidgets = models.CharField(max_length=100, verbose_name='ویژگی های خاص', choices=(
        ("روباری", "روباری"),
        ("نیاز به بارنامه ندارد", "نیاز به بارنامه ندارد"),
        ("بارنامه خودم میگیرم", "بارنامه خودم میگیرم"),
    ))
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
    ))
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
    ))
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


class RoadFleet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
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
    semiHeavyVehichle = models.CharField(max_length=20, verbose_name="ماشین باربری نیمه سنگین ", default="",
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

    carrier_in = models.BooleanField(verbose_name="حمل و نقل داخلی", default="")
    carrier_out = models.BooleanField(verbose_name="حمل و نقل بین المللی", default="")

    class Meta:
        verbose_name = "ناوگان جاده ای"

    def __str__(self):
        return self.ownerType


# Model for the request of transportation from a driver
class CarrierReqToDriver(Base_Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_carrier_requests',
                               verbose_name='راننده')
    carrier = models.ForeignKey(RoadFleet, on_delete=models.CASCADE, verbose_name='حمل‌کننده')
    carrier_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_requests',
                                      verbose_name='صاحب حمل‌کننده')
    collaboration_type = models.CharField(max_length=20, default="full_time", verbose_name='نوع همکاری',
                                          choices=(
                                              ('full_time', 'تمام وقت'),
                                              ('part_time', 'پاره وقت/بار موردی'),
                                          ))
    proposed_price = models.FloatField(default=0, verbose_name='قیمت پیشنهادی')
    origin = models.CharField(max_length=100, blank=True, null=True, verbose_name='مبدا بار ')

    # Additional features based on the type of collaboration
    destination = models.CharField(max_length=100, verbose_name='مقصد بار ', blank=True, null=True)
    arrival_date_at_origin = models.DateField(verbose_name='تاریخ حضور در مبدا', blank=True, null=True)

    class Meta:
        verbose_name = 'درخواست صاحب حمل‌کننده از راننده'
        verbose_name_plural = "درخواست های صاحب حمل‌کننده از راننده"


# Model for the request of a carrier owner to a driver
class CarrierReqToGoodsOwner(Base_Model):
    CARGO_TYPE_CHOICES = [
        ('inner_cargo', 'اعلام بار داخلی'),
        ('international_cargo', 'اعلام بار خارجی'),
        ('rail_cargo', 'اعلام بار ریلی'),
    ]

    cargo_type = models.CharField(max_length=20, default='inner_cargo', choices=CARGO_TYPE_CHOICES,
                                  verbose_name='نوع همکاری')
    carrier_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goods_owner_requests',
                                      verbose_name='صاحب حمل‌کننده')
    carrier = models.ForeignKey(RoadFleet, on_delete=models.CASCADE, verbose_name='حمل‌کننده')
    goods_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goods_owner_carrier_requests',
                                    verbose_name='صاحب بار')
    inner_cargo = models.ForeignKey(InnerCargo, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='بار داخلی')
    international_cargo = models.ForeignKey(InternationalCargo, on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name='بار خارجی')

    price = models.FloatField(default=0, verbose_name='قیمت پیشنهادی', )

    class Meta:
        verbose_name = 'درخواست صاحب حمل‌کننده به  صاحب بار'
        verbose_name_plural = "درخواست های صاحب حمل‌کننده به صاحب بار"
