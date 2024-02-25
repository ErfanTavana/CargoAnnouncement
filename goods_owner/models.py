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
from carrier_owner.models import CarrierOwner

# CHOICES برای نتایج ممکن برای درخواست همکاری
REQUEST_RESULT_CHOICES = [
    ('در انتظار پاسخ', 'در انتظار پاسخ'),
    ('تایید شده', 'تایید شده'),
    ('رد شده', 'رد شده'),
    ('لغو شده', 'لغو شده'),
]


# تابع برای ایجاد یک شناسه پیچیده تصادفی
def generate_complex_id():
    id_length = 8  # طول شناسه پیچیده تولیدی
    characters = string.ascii_letters + string.digits  # مجموعه کاراکترها (حروف و ارقام) برای انتخاب
    complex_id = ''.join(
        random.choice(characters) for _ in range(id_length))  # تولید شناسه پیچیده با استفاده از کاراکترهای تصادفی
    return complex_id  # بازگشت شناسه پیچیده تولید شده


# کلاس پایه برای فیلدهای مشترک بین مدل‌های مختلف
class Base_Model(models.Model):
    id = models.CharField(primary_key=True, default=generate_complex_id, max_length=10, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ ایجاد')
    deleted_at = models.DateTimeField(default=None, null=True, blank=True, verbose_name='تاریخ حذف')
    is_ok = models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')
    is_changeable = models.BooleanField(default=True, verbose_name='قابل تغییر است؟')
    is_deletable = models.BooleanField(default=True, verbose_name='قابل حذف است؟')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='deleted_by_%(class)s_set', verbose_name='حذف شده توسط ')

    class Meta:
        abstract = True  # نشان می‌دهد که این کلاس یک کلاس انتزاعی است و نباید یک جدول در پایگاه داده ایجاد کند

    def soft_delete(self, deleted_by):
        self.deleted_at = timezone.now()
        self.is_ok = False
        self.is_changeable = False
        self.deleted_by = deleted_by
        self.is_deletable = False
        self.save()


# کلاس بار مشترک
class CommonCargo(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    goods_owner = models.ForeignKey(GoodsOwner, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='پروفایل صاحب بار')

    # فیلدهای مشترک
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

    # فیلدهای ارائه‌دهنده تحویل
    delivery_provider_name = models.CharField(max_length=100, verbose_name="نام شرکت تحویل دهنده", blank=True,
                                              null=True)
    delivery_provider_national_id = models.CharField(max_length=20, verbose_name="شناسه ملی تحویل دهنده", blank=True,
                                                     null=True)
    delivery_provider_full_name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی تحویل دهنده",
                                                   blank=True, null=True)
    delivery_provider_mobile = models.CharField(max_length=12, verbose_name="شماره موبایل مدیر عامل تحویل دهنده",
                                                blank=True, null=True)

    # فیلدهای گیرنده بار
    cargo_receiver_name = models.CharField(max_length=100, verbose_name="نام شرکت تحویل گیرنده", blank=True, null=True)
    cargo_receiver_national_id = models.CharField(max_length=20, verbose_name="شناسه ملی تحویل گیرنده", blank=True,
                                                  null=True)
    cargo_receiver_full_name = models.CharField(max_length=200, verbose_name="نام و نام خانوادگی تحویل گیرنده",
                                                blank=True, null=True)
    cargo_receiver_mobile = models.CharField(max_length=12, verbose_name="شماره موبایل مدیر عامل تحویل گیرنده",
                                             blank=True, null=True)
    # Comment: فیلدهای منحصر به فرد برای InnerCargo
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

    cargo_receiver_surname = models.CharField(max_length=100, verbose_name="نام خانوادگی تحویل گیرنده", blank=True,
                                              null=True)
    destination_country = models.CharField(max_length=20, verbose_name="کشور مقصد", blank=True, null=True, choices=(
        ("ایران", "ایران"),
        ("روسیه", "روسیه"),
        ("قزاقستان", "قزاقستان"),
        ("ازبکستان", "ازبکستان"),
        ("قرقیزستان", "قرقیزستان"),
        ("تاجیکستان", "تاجیکستان"),
        ("افغانستان", "افغانستان"),
        ("ارمنستان", "ارمنستان"),
    ))
    destination_state = models.CharField(max_length=20, verbose_name="استان مقصد", blank=True, null=True)
    destination_city = models.CharField(max_length=20, verbose_name="شهر / منطقه / محدوده مقصد", blank=True, null=True)
    destination_street = models.CharField(max_length=50, verbose_name="خیابان مقصد", blank=True, null=True)
    destination_address = models.CharField(max_length=100, verbose_name="آدرس دقیق مقصد", blank=True, null=True)
    destination_area = models.CharField(max_length=100, choices=(
        ('گمرگ', 'گمرگ'),
        ('بندر', 'بندر'),
        ('ایستگاه', 'ایستگاه'),
    ), verbose_name='محدوده مقصد', blank=True, null=True)
    destination_custom_name = models.CharField(max_length=100, verbose_name="نام کمرگ مقصد", default="", blank=True,
                                               null=True)
    is_bulk_cargo = models.BooleanField(default=False, verbose_name="آیا بار شما خرده بار است؟")
    bulk_cargo_tonnage = models.FloatField(verbose_name="تناژ خرده بار", default=0, blank=True, null=True)
    is_plannable = models.BooleanField(default=False, verbose_name="آیا بار شما قابلیت برنامه‌ریزی دارد؟")
    weekly_days = models.CharField(max_length=50, verbose_name="روزهای هفته", blank=True, null=True)
    is_perishable = models.BooleanField(default=False, verbose_name="آیا بار شما فسادپذیر است؟")
    refrigeration_temperature = models.FloatField(default=0, verbose_name="دمای سردخانه")
    is_hazardous = models.BooleanField(default=False, verbose_name="آیا بار شما خطرناک است؟")
    un_code = models.CharField(max_length=20, verbose_name="کد UN (کد کالای خطرناک)", blank=True, null=True)
    customs_hs_code = models.CharField(max_length=20, verbose_name="کد HS گمرکی", blank=True, null=True)

    class Meta:
        verbose_name = 'اعلام بار اطلاعات  مشترک'
        abstract = True


# کلاس بار داخلی که از کلاس CommonCargo ارث‌بری می‌کند
class InnerCargo(CommonCargo):
    deliveryTimeDate = models.DateTimeField(
        max_length=200,
        verbose_name="تاریخ و ساعت تحویل بار در مبدا",
        default=timezone.now,
        blank=True,
        null=True,
    )
    dischargeTimeDate = models.DateTimeField(max_length=200, verbose_name="تاریخ و ساعت تحویل بار در مقصد",
                                             default=timezone.now, blank=True, null=True)

    class Meta:
        verbose_name = 'اعلام بار داخلی'
        verbose_name_plural = 'اعلام بار های  داخلی'


# کلاس بار بین‌المللی که از کلاس CommonCargo ارث‌بری می‌کند
class InternationalCargo(CommonCargo):
    senderCountry = models.CharField(max_length=255, verbose_name="کشور مبدا", choices=(
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
    deliveryTimeDate = models.DateTimeField(max_length=200, verbose_name="تاریخ و ساعت بارگیری بار در مبدا",
                                            default=timezone.now, blank=True, null=True)
    dischargeTimeDate = models.DateTimeField(max_length=200, verbose_name="تاریخ و ساعت تحویل بار در مقصد",
                                             default=timezone.now, blank=True, null=True)
    dischargeTime = models.DurationField(max_length=200, verbose_name="مدت زمان تخلیه بار در مقصد",
                                         default=timezone.timedelta(hours=0, minutes=0, seconds=0), blank=True,
                                         null=True)
    # customName = models.CharField(max_length=100, verbose_name="نام کمرگ مبدا", default="", blank=True, null=True)
    customNameEnd = models.CharField(max_length=100, verbose_name="نام کمرگ مقصد", default="", blank=True, null=True)
    cargo_weight = models.FloatField(max_length=100, verbose_name="وزن خالص محموله", blank=True, null=True)

    class Meta:
        verbose_name = 'اعلام بار خارجی'
        verbose_name_plural = 'اعلام بار های خارجی'


# کلاس مدل بار مورد نیاز که از کلاس Base_Model ارث‌بری می‌کند
class RequiredCarrier(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    goods_owner = models.ForeignKey(GoodsOwner, on_delete=models.CASCADE, blank=True, null=True)
    relinquished = models.BooleanField(default=False, verbose_name="واگذار شده؟")
    CARGO_TYPE_CHOICES = [
        ('اعلام بار داخلی', 'اعلام بار داخلی'),
        ('اعلام بار خارجی', 'اعلام بار خارجی'),
        ('اعلام بار ریلی', 'اعلام بار ریلی'),
    ]
    cargo_type = models.CharField(max_length=20, choices=CARGO_TYPE_CHOICES, verbose_name='نوع بار')
    inner_cargo = models.ForeignKey(InnerCargo, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='اعلام بار داخلی', related_name='inner_cargo_carriers')
    international_cargo = models.ForeignKey(InternationalCargo, blank=True, null=True, on_delete=models.CASCADE,
                                            verbose_name='اعلام بار خارجی', related_name='international_cargo_carriers')

    cargo_weight = models.FloatField(max_length=100, verbose_name="وزن خالص محموله", blank=True, null=True)
    counter = models.PositiveIntegerField(verbose_name="تعداد حمل کننده مورد نیاز", blank=True, null=True)
    room_type = models.CharField(max_length=100, verbose_name="نوع اتاق مناسب", choices=(
        ("چادری", "چادری"),
        ("روباز", "روباز"),
        ("یخچالی", "یخچالی"),
    ), blank=True, null=True)
    vehichle_type = models.CharField(max_length=100, verbose_name="نوع وسیله حمل کننده مورد نیاز", choices=(
        ("ماشین باربری کوچک و سبک", "ماشین باربری کوچک و سبک"),
        ("ماشین باربری نیمه سنگین", "ماشین باربری نیمه سنگین"),
        ("ماشین حمل بار سنگین", "ماشین حمل بار سنگین"),
    ), blank=True, null=True)

    semi_heavy_vehichle = models.CharField(max_length=20, verbose_name="ماشین باربری نیمه سنگین ", choices=(
        ("کامیون", "کامیون"),
        ("خاور", "خاور"),
        ("هیوندا", "هیوندا"),
        ("ماشین باربری ایسوزو", "ماشین باربری ایسوزو"),
        ("کامیونت", "کامیونت"),
    ), blank=True, null=True)
    semi_heavy_vehichle_others = models.CharField(max_length=100, verbose_name="سایر", default="", blank=True,
                                                  null=True)

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
    ), blank=True, null=True)
    heavy_vehichle_others = models.CharField(max_length=100, verbose_name="سایر", default="", blank=True, null=True)

    special_widget_carrier = models.TextField(max_length=9999, verbose_name="ویژگی های خاص حمل کننده مورد نیاز",
                                              blank=True, null=True)
    carrier_price = models.IntegerField(default=0, verbose_name="قیمت تقریبی حمل", blank=True, null=True)

    # فیلدهای مختص به حمل بین المللی
    cargo_price = models.PositiveIntegerField(default=0, verbose_name="ارزش بار هر حمل کننده / خودرو", blank=True,
                                              null=True)

    transferred_to = models.ForeignKey(User, related_name='transferred_to_%(class)s_set', verbose_name="واگذار شده به",
                                       on_delete=models.CASCADE, blank=True,
                                       null=True)
    transferred_at = models.DateTimeField(default=None, verbose_name="واگذار شده در تاریخ", blank=True, null=True)

    def Transferred(self, User):
        self.transferred_to = User.id
        self.transferred_at = timezone.now()
        self.save()

    class Meta:
        verbose_name = 'حمل‌کننده مورد نیاز اعلام بار'
        verbose_name_plural = 'حمل‌کننده‌های مورد نیاز اعلام بار'


class GoodsOwnerReqCarOw(Base_Model):
    user = models.ForeignKey(User, on_delete=models.Model, verbose_name='کاربر', related_name='userss', )
    goods_owner = models.ForeignKey(GoodsOwner, related_name='goods_owner_requests', on_delete=models.CASCADE,
                                    verbose_name='صاحب بار', blank=True, null=True)

    carrier_owner = models.ForeignKey(CarrierOwner, related_name='carrier_owner_requests', on_delete=models.CASCADE,
                                      verbose_name='صاحب  حمل کننده', blank=True, null=True)
    road_fleet = models.ForeignKey('carrier_owner.RoadFleet', related_name='road_fleet_fleetasad',
                                   verbose_name='حمل کننده',
                                   on_delete=models.CASCADE, blank=True, null=True)

    inner_cargo = models.ForeignKey(InnerCargo, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='اعلام بار داخلی', related_name='inner_cargo_carriers2')
    international_cargo = models.ForeignKey(InternationalCargo, blank=True, null=True, on_delete=models.CASCADE,
                                            verbose_name='اعلام بار خارجی',
                                            related_name='international_cargo_carriers2')

    # قیمت پیشنهادی
    proposed_price = models.FloatField(default=0.0, verbose_name='قیمت پیشنهادی', blank=True, null=True)

    # نتیجه درخواست
    request_result = models.CharField(max_length=30, choices=REQUEST_RESULT_CHOICES, verbose_name='نتیجه درخواست')
    # زمان لغو درخواست
    cancellation_time = models.DateTimeField(null=True, blank=True, verbose_name='زمان لغو درخواست')

    class Meta:
        verbose_name = 'درخواست همکاری صاحب بار برای صاحب حمل کننده'
        verbose_name_plural = 'درخواست های همکاری صاحب بار برای صاحب حمل کننده'


VEHICLE_TYPE_CHOICES = (
    ('short_edge', 'لبه کوتاه'),
    ('long_edge', 'لبه بلند'),
    ('covered', 'مسقف'),
    ('flatbed', 'مسطح یا پلتفرم'),
)
from django.db import models
from django.contrib.auth.models import User


class CargoDeclaration(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    goods_owner = models.ForeignKey(GoodsOwner, on_delete=models.CASCADE, blank=True, null=True)
    relinquished = models.BooleanField(default=False, verbose_name="واگذار شده؟")
    CARGO_TYPE_CHOICES = [
        ('اعلام بار داخلی', 'اعلام بار داخلی'),
        ('اعلام بار خارجی', 'اعلام بار خارجی'),
        ('اعلام بار ریلی', 'اعلام بار ریلی'),
    ]
    cargo_type = models.CharField(max_length=20, choices=CARGO_TYPE_CHOICES, verbose_name='نوع بار')
    inner_cargo = models.ForeignKey(InnerCargo, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='اعلام بار داخلی', related_name='inner_cargo_carriers_%(class)s_set')
    international_cargo = models.ForeignKey(InternationalCargo, blank=True, null=True, on_delete=models.CASCADE,
                                            verbose_name='اعلام بار خارجی',
                                            related_name='international_cargo_carriers_%(class)s_set')
    # وزن خالص محموله
    net_weight = models.FloatField(verbose_name="وزن خالص محموله")

    # ویژگی های خاص مورد نیاز (تکست فیلد)
    special_features = models.TextField(verbose_name="ویژگی‌های خاص مورد نیاز")

    # قیمت تقریبی حمل (فلوت فیلد)
    approximate_transport_price = models.FloatField(verbose_name="قیمت تقریبی حمل")

    # ارزش بار هر واگن (فلوت فیلد)
    value_per_wagon = models.FloatField(verbose_name="ارزش بار هر واگن")

    # انواع واگن
    WAGON_TYPES = [
        ('short_edge', 'لبه کوتاه'),
        ('tall_edge', 'لبه بلند'),
        ('covered', 'مسقف'),
        ('flatbed', 'مسطح یا پلتفرم'),
        ('open_roof', 'روباز'),
        ('bulk', 'فله بر'),
        ('refrigerated', 'یخچال دار'),
        ('tanker', 'مخزن دار'),
        ('sand_carrier', 'شن کش'),
        ('car_transport', 'حمل خودرو'),
    ]
    wagon_type = models.CharField(max_length=20, choices=WAGON_TYPES, verbose_name="نوع واگن")

    # کد مسیر
    route_code = models.CharField(max_length=50, verbose_name="کد مسیر")

    # کد ایستگاه
    station_code = models.CharField(max_length=50, verbose_name="کد ایستگاه")

    # آیا بار شما قابلیت برنامه‌ریزی دارد؟ (بولین)
    is_plannable = models.BooleanField(default=False, verbose_name="آیا بار قابل برنامه‌ریزی است؟")

    # تناژ در هر نوبت
    tonnage_per_shift = models.FloatField(verbose_name="تناژ در هر نوبت")

    # آیا بار شما خرده بار است؟ (بولین)
    is_partial_cargo = models.BooleanField(default=False, verbose_name="آیا بار خرده بار است؟")

    # تناژ
    tonnage = models.FloatField(blank=True, null=True, verbose_name="تناژ")

    # نوع بار (کرفیلد)
    cargo_type_char_field = models.CharField(blank=True, null=True, max_length=255, verbose_name="نوع بار")

    class Meta:
        verbose_name = 'واگن  مورد نیاز اعلام بار'
        verbose_name_plural = 'واگن های مورد نیاز اعلام بار'

    def __str__(self):
        return f"بار شماره {self.id}"
