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
from accounts.models import WagonOwner

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
        ('درخواست بارنامه', 'درخواست بارنامه'),
    ), blank=True, null=True)
    specialDesc = models.TextField(max_length=9999, verbose_name="توضیحات خاص", default="", blank=True, null=True)
    sendersName = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی فرستنده", default="", blank=True,
                                   null=True)
    senderMobileNum = models.CharField(max_length=12, verbose_name="شماره تلفن / موبایل فرستنده", default="",
                                       blank=True, null=True)
    dischargeTimeDate = models.DateTimeField(max_length=200, verbose_name="حدود تاریخ و ساعت تحویل بار در مقصد",
                                             default=timezone.now, blank=True, null=True)
    duratio_ndischargeTime = models.DurationField(max_length=200, verbose_name=" مدت زمان تخلیه بار در مقصد",
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
        ("افغانستان", "افغانستان"),
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
        ('گمرک', 'گمرک'),
        ('بندر', 'بندر'),
        ('ایستگاه', 'ایستگاه'),
        ('گمرک/ایستگاه', 'گمرک/ایستگاه'),
    ), verbose_name='محدوده مقصد', blank=True, null=True)
    destination_custom_name = models.CharField(max_length=100, verbose_name="نام  مقصد", default="", blank=True,
                                               null=True)
    is_bulk_cargo = models.BooleanField(default=False, verbose_name="آیا بار شما خرده بار است؟")
    bulk_cargo_tonnage = models.FloatField(verbose_name="تناژ خرده بار", default=0, blank=True, null=True)
    is_plannable = models.BooleanField(default=False, verbose_name="آیا بار شما قابلیت برنامه‌ریزی دارد؟")
    weekly_days = models.CharField(max_length=100, verbose_name="روزهای هفته", blank=True, null=True)
    is_perishable = models.BooleanField(default=False, blank=True, null=True, verbose_name="آیا بار شما فسادپذیر است؟")
    refrigeration_temperature = models.FloatField(default=0, verbose_name="دمای سردخانه")
    is_hazardous = models.BooleanField(default=False, verbose_name="آیا بار شما خطرناک است؟")
    un_code = models.CharField(max_length=20, verbose_name="کد UN (کد کالای خطرناک)", blank=True, null=True)
    customs_hs_code = models.CharField(max_length=20, verbose_name="کد HS گمرکی", blank=True, null=True)

    pallet_size = models.CharField(max_length=100, verbose_name="سایز پالت (مشخصات بسته بندی)", blank=True, null=True)
    pallet_arrangement_type = models.CharField(max_length=50, verbose_name="نوع چیدمان پالت", choices=(
        ("کف", "کف"),
        ("طبقاتی", "طبقاتی"),
    ), blank=True, null=True)
    approximate_weight_per_packaging = models.FloatField(verbose_name="وزن حدودی هر یک بسته بندی", blank=True,
                                                         null=True)
    is_all_cargo_type = models.BooleanField(default=False, verbose_name="آیا تمام بار تیپ است؟")
    approximate_weight_per_type = models.FloatField(verbose_name="وزن حدودی هر تیپ", blank=True, null=True)
    specialized_lashing_required = models.BooleanField(default=False,
                                                       verbose_name="آیا بار نیاز به مهار بندی تخصصی دارد؟")
    specialized_lashing_type_upload = models.ImageField(upload_to='lashing_types/', blank=True, null=True,
                                                        verbose_name="آپلود نوع مهار بندی تخصصی")
    specialized_lashing_type_description = models.TextField(max_length=5000,
                                                            verbose_name="توضیح نوع مهار بندی تخصصی", blank=True,
                                                            null=True)
    need_warehouse = models.BooleanField(default=False, verbose_name="آیا نیاز به انبار دارید؟")
    warehouse_duration = models.DurationField(verbose_name="مدت زمان انبار داری", blank=True, null=True)
    sender_additional_requests = models.TextField(max_length=5000, verbose_name="درخواست های تکمیلی فرستنده",
                                                  blank=True, null=True)
    cargo_procedure_type = models.CharField(max_length=20, verbose_name="نوع رویه بار", choices=(
        ("صادراتی", "صادراتی"),
        ("وارداتی", "وارداتی"),
        ("ترانزیتی", "ترانزیتی"),
    ), blank=True, null=True)
    need_route_code = models.BooleanField(default=False, verbose_name="آیا نیاز به کد مسیر دارید؟")
    route_code = models.CharField(max_length=20, verbose_name="کد مسیر", blank=True, null=True)

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
        ("افغانستان", "افغانستان"),
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
        ("کمپرسی", "کمپرسی"),
        ("مسقف", "مسقف"),
        ("کفی", "کفی"),
        ("بفل دار", "بقل دار"),

    ), blank=True, null=True)
    vehichle_type = models.CharField(max_length=100, verbose_name="نوع وسیله حمل کننده مورد نیاز", choices=(
        ("تریلی", "تریلی"),
        ("جفت", "جفت"),
        ("تک", "تک"),
        ("خاور", "خاور"),
        ("وانت و نیسان", "وانت ونیسان"),
        ("خاور", "خاور"),
    ), blank=True, null=True)

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


class CargoFleetCoordination(Base_Model):
    inner_cargo = models.ForeignKey(InnerCargo, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='اعلام بار داخلی')
    international_cargo = models.ForeignKey(InternationalCargo, on_delete=models.CASCADE, blank=True, null=True,
                                            verbose_name='اعلام بار خارجی')
    required_carrier = models.ForeignKey(RequiredCarrier, on_delete=models.CASCADE, blank=True, null=True,
                                         verbose_name='حمل کننده ی مورد نیاز اعلام بار')
    road_fleet = models.ForeignKey('carrier_owner.RoadFleet', on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='حمل کننده')
    status_result = models.CharField(max_length=100,
                                     choices=(
                                         ('واگذار شده', 'وارگذار شده'), ('در انتظار واگذاری', 'در انتظار واگذاری')),
                                     verbose_name='وضعیت نتیجه', default='در انتظار واگذاری')

    class Meta:
        verbose_name = 'ماشین  مورد نیاز و ارتباطات'
        verbose_name_plural = 'ماشین های مورد نیاز و ارتباطات'


VEHICLE_TYPE_CHOICES = (
    ('short_edge', 'لبه کوتاه'),
    ('long_edge', 'لبه بلند'),
    ('covered', 'مسقف'),
    ('flatbed', 'مسطح یا پلتفرم'),
)


class RailCargo(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    goods_owner = models.ForeignKey(GoodsOwner, blank=True, null=True, on_delete=models.CASCADE,
                                    verbose_name='پروفایل صاحب بار')
    APPROVAL_STATUS_CHOICES = [
        ('در انتظار پاسخ', 'در انتظار پاسخ'),
        ('تایید شده', 'تایید شده'),
        ('رد شده', 'رد شده'),
    ]
    approval_status = models.CharField(
        max_length=20, choices=APPROVAL_STATUS_CHOICES,
        verbose_name='تایید یا رد توسط اتحادیه صادرکنندگان', default='در انتظار پاسخ', blank=True, null=True
    )
    approval_date_time = models.DateTimeField(
        verbose_name='تاریخ و ساعت تایید یا رد', blank=True, null=True
    )
    approved_rejected_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='approved_rejected_wagons', verbose_name='تایید یا رد توسط کاربر'
    )
    rejection_reason = models.TextField(
        verbose_name='شرح دلیل رد شدن درخواست', blank=True, null=True
    )

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

    specialDesc = models.TextField(max_length=9999, verbose_name="توضیحات خاص", default="", blank=True, null=True)
    sendersName = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی فرستنده", default="", blank=True,
                                   null=True)
    senderMobileNum = models.CharField(max_length=12, verbose_name="شماره تلفن / موبایل فرستنده", default="",
                                       blank=True, null=True)
    dischargeTimeDate = models.DateTimeField(max_length=200, verbose_name="حدود تاریخ و ساعت تحویل بار در مقصد",
                                             default=timezone.now, blank=True, null=True)
    duratio_ndischargeTime = models.DurationField(max_length=200, verbose_name=" مدت زمان تخلیه بار در مقصد",
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
        ("افغانستان", "افغانستان"),
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
        ('گمرک', 'گمرک'),
        ('بندر', 'بندر'),
        ('ایستگاه', 'ایستگاه'),
        ('گمرک/ایستگاه', 'گمرک/ایستگاه'),
    ), verbose_name='محدوده مقصد', blank=True, null=True)
    destination_custom_name = models.CharField(max_length=100, verbose_name="نام  مقصد", default="", blank=True,
                                               null=True)
    is_bulk_cargo = models.BooleanField(default=False, verbose_name="آیا بار شما خرده بار است؟")
    bulk_cargo_tonnage = models.FloatField(verbose_name="تناژ خرده بار", default=0, blank=True, null=True)
    is_plannable = models.BooleanField(default=False, verbose_name="آیا بار شما قابلیت برنامه‌ریزی دارد؟")
    weekly_days = models.CharField(max_length=100, verbose_name="روزهای هفته", blank=True, null=True)
    is_perishable = models.BooleanField(default=False, blank=True, null=True, verbose_name="آیا بار شما فسادپذیر است؟")
    refrigeration_temperature = models.FloatField(default=0, verbose_name="دمای سردخانه")
    is_hazardous = models.BooleanField(default=False, verbose_name="آیا بار شما خطرناک است؟")
    un_code = models.CharField(max_length=20, verbose_name="کد UN (کد کالای خطرناک)", blank=True, null=True)
    customs_hs_code = models.CharField(max_length=20, verbose_name="کد HS گمرکی", blank=True, null=True)

    pallet_size = models.CharField(max_length=100, verbose_name="سایز پالت (مشخصات بسته بندی)", blank=True, null=True)
    pallet_arrangement_type = models.CharField(max_length=50, verbose_name="نوع چیدمان پالت", choices=(
        ("کف", "کف"),
        ("طبقاتی", "طبقاتی"),
    ), blank=True, null=True)
    approximate_weight_per_packaging = models.FloatField(verbose_name="وزن حدودی هر یک بسته بندی", blank=True,
                                                         null=True)
    is_all_cargo_type = models.BooleanField(default=False, verbose_name="آیا تمام بار تیپ است؟")
    approximate_weight_per_type = models.FloatField(verbose_name="وزن حدودی هر تیپ", blank=True, null=True)
    specialized_lashing_required = models.BooleanField(default=False,
                                                       verbose_name="آیا بار نیاز به مهار بندی تخصصی دارد؟")
    specialized_lashing_type_upload = models.ImageField(upload_to='lashing_types/', blank=True, null=True,
                                                        verbose_name="آپلود نوع مهار بندی تخصصی")
    specialized_lashing_type_description = models.TextField(max_length=5000,
                                                            verbose_name="توضیح نوع مهار بندی تخصصی", blank=True,
                                                            null=True)
    need_warehouse = models.BooleanField(default=False, verbose_name="آیا نیاز به انبار دارید؟")
    warehouse_duration = models.DurationField(verbose_name="مدت زمان انبار داری", blank=True, null=True)
    sender_additional_requests = models.TextField(max_length=5000, verbose_name="درخواست های تکمیلی فرستنده",
                                                  blank=True, null=True)
    cargo_procedure_type = models.CharField(max_length=20, verbose_name="نوع رویه بار", choices=(
        ("صادراتی", "صادراتی"),
        ("وارداتی", "وارداتی"),
        ("ترانزیتی", "ترانزیتی"),
    ), blank=True, null=True)
    need_route_code = models.BooleanField(default=False, verbose_name="آیا نیاز به کد مسیر دارید؟")
    route_code = models.CharField(max_length=20, verbose_name="کد مسیر", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.cargo_procedure_type != 'صادراتی':
            self.approval_status = 'تایید شده'
            self.approval_date_time = timezone.now()
            self.approved_rejected_by = self.user
            self.rejection_reason = 'فقط بار های صادراتی نیاز به تایید اتحادیه صادرکنندگان دارند'
        super(RailCargo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'اعلام بار ریلی'
        verbose_name_plural = 'اعلام بار های ریلی'


class RequiredWagons(Base_Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', blank=True, null=True)
    goods_owner = models.ForeignKey(GoodsOwner, on_delete=models.CASCADE, blank=True, null=True)
    relinquished = models.BooleanField(default=False, verbose_name="واگذار شده؟")
    CARGO_TYPE_CHOICES = [
        ('اعلام بار داخلی', 'اعلام بار داخلی'),
        ('اعلام بار خارجی', 'اعلام بار خارجی'),
        ('اعلام بار ریلی', 'اعلام بار ریلی'),
    ]
    cargo_type = models.CharField(max_length=20, choices=CARGO_TYPE_CHOICES, verbose_name='نوع بار')
    rail_cargo = models.ForeignKey(RailCargo, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name='اعلام بار ریلی', related_name='rail_cargo_related_name')
    wagon_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='نوع واگن',
                                  choices=(
                                      ("مسقف", "مسقف"),
                                      ("فله بر", "فله بر"),
                                      ("مسطح", "مسطح"),
                                      ("یخچال دار", "یخچال دار"),
                                      ("مخزن دار", "مخزن دار"),
                                      ("لبه بلند", "لبه بلند"),
                                      ("لبه کوتاه", "لبه کوتاه"),
                                      ("حمل خودرو", "حمل خودرو"),))
    capacity = models.CharField(max_length=20, blank=True, null=True, verbose_name="ظرفیت حمل", default="",
                                choices=(
                                    ("واگن 24", "واگن 24"),
                                    ("واگن 26", "واگن 26"),
                                    ("واگن 28", "واگن 28"),
                                    ("واگن 29", "واگن 29"),
                                    ("سایر", "سایر"),))
    net_weight = models.FloatField(verbose_name="وزن خالص محموله", blank=True, null=True)
    counter = models.IntegerField(verbose_name="تعداد واگن", default=0)

    class Meta:
        verbose_name = 'واگن مورد نیاز'
        verbose_name_plural = 'واگن های مورد نیاز'


class CargoWagonCoordination(Base_Model):
    rail_cargo = models.ForeignKey(RailCargo, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name='اعلام بار ریلی')
    required_wagons = models.ForeignKey(RequiredWagons, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name='واگن مورد نیاز')
    wagon_owner = models.ForeignKey(WagonOwner, on_delete=models.CASCADE, blank=True, null=True,
                                    verbose_name='صاحب واگن')
    status_result = models.CharField(max_length=100,
                                     choices=(
                                         ('واگذار شده', 'وارگذار شده'), ('در انتظار واگذاری', 'در انتظار واگذاری')),
                                     verbose_name='وضعیت نتیجه', default='در انتظار واگذاری')

    class Meta:
        verbose_name = 'واگن  مورد نیاز و ارتباطات'
        verbose_name_plural = 'واگن  های مورد نیاز و ارتباطات'
