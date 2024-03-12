from django.db import models
from goods_owner.models import Base_Model


class HomePageInfo(Base_Model):
    num_sessions = models.IntegerField(verbose_name='تعداد جلسات آموزش', default=0)
    num_participants = models.IntegerField(verbose_name='تعداد شرکت‌کنندگان', default=0)
    training_hours = models.IntegerField(verbose_name='تعداد ساعات آموزش', default=0)
    completed_projects = models.IntegerField(verbose_name='تعداد پروژه‌های تکمیل شده', default=0)
    qrcode_image = models.ImageField(verbose_name='عکس کیو آر کد', upload_to='qrcodes/', null=True, blank=True)
    ready_to_work_drivers = models.PositiveIntegerField(blank=True, null=True,
                                                        verbose_name='تعداد راننده‌های آماده به کار')
    distance_covered = models.PositiveIntegerField(blank=True, null=True, verbose_name='کیلومتر مسیر طی شده')
    loads_carried = models.PositiveIntegerField(blank=True, null=True, verbose_name='تعداد بار حمل شده')
    country = models.CharField(blank=True, null=True, max_length=100, verbose_name='کشور')
    province = models.CharField(blank=True, null=True, max_length=100, verbose_name='استان')
    city = models.CharField(blank=True, null=True, max_length=100, verbose_name='شهر')
    address = models.TextField(blank=True, null=True, verbose_name='آدرس')
    full_address = models.TextField(blank=True, null=True, verbose_name='آدرس کامل')
    phone_prefix = models.CharField(blank=True, null=True, max_length=5, verbose_name='پیش‌ شماره')
    phone_number = models.CharField(blank=True, null=True, max_length=15, verbose_name='شماره تلفن')
    email = models.EmailField(blank=True, null=True, verbose_name='ایمیل')
    working_days = models.CharField(blank=True, null=True, max_length=50, verbose_name='روزهای کاری')
    telegram_address = models.URLField(blank=True, null=True, verbose_name='آدرس تلگرام')
    whatsapp_address = models.URLField(blank=True, null=True, verbose_name='آدرس واتساپ')
    instagram_address = models.URLField(blank=True, null=True, verbose_name='آدرس اینستاگرام')
    facebook_address = models.URLField(blank=True, null=True, verbose_name='آدرس فیسبوک')
    android_app = models.FileField(blank=True, null=True, verbose_name=' نرم‌افزار اندروید')
    web_app_address = models.URLField(blank=True, null=True, verbose_name='آدرس وب اپلیکیشن')
    whatsapp_mz = models.URLField(blank=True, null=True, verbose_name='آدرس واتساپ MZ')
    linkedin_mz = models.URLField(blank=True, null=True, verbose_name='لینکدین MZ')
    instagram_mz = models.URLField(blank=True, null=True, verbose_name='آدرس اینستاگرام MZ')
    telegram_mz = models.URLField(blank=True, null=True, verbose_name='آدرس تلگرام MZ')
    vichat_mz = models.URLField(blank=True, null=True, verbose_name='ویچت MZ')
    rail_cargo_payment_rate = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name='نرخ پرداختی بار ریلی'
    )

    domestic_truck_payment_rate = models.IntegerField(
        blank=True,
        null=True,
        default=0,

        verbose_name='نرخ پرداختی اعلام بار'
    )

    wagon_owner_payment_rate = models.IntegerField(
        blank=True,
        null=True,
        default=0,

        verbose_name='نرخ پرداختی صاحب واگن'
    )

    carrier_owner_payment_rate = models.IntegerField(
        blank=True,
        null=True,
        default=0,

        verbose_name='نرخ پرداختی صاحب حمل‌کننده'
    )

    driver_payment_rate = models.IntegerField(
        blank=True,
        null=True,
        default=0,

        verbose_name='نرخ پرداختی راننده'
    )
    exporters_union_payment_rate = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='نرخ پرداختی اتحادیه صادرکنندگان',
    )

    def __str__(self):
        return f'{self.country} - {self.province} - {self.city}'

    def save(self, *args, **kwargs):
        # ایجاد آدرس کامل با استفاده از سایر فیلدها
        full_address_parts = [self.country, self.province, self.city, self.address]
        full_address_parts = [part for part in full_address_parts if part]  # حذف مقادیر خالی
        self.full_address = ', '.join(full_address_parts)

        # فراخوانی متد save اصلی
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'اطلاعات صفحه ی اصلی'
        verbose_name_plural = 'اطلاعات های صفحه ی اصلی'
