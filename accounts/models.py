from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import string
import random
from rest_framework.authtoken.models import Token


# Function to generate a random complex ID
def generate_complex_id():
    id_length = 8  # Length of the generated complex ID
    characters = string.ascii_letters + string.digits  # Set of characters (letters and digits) to choose from
    complex_id = ''.join(
        random.choice(characters) for _ in range(id_length))  # Generate the complex ID using random characters
    return complex_id  # Return the generated complex ID


# Base_Model Class
# کلاس ابتدایی برای فیلدهای مشترک بین مدل‌های مختلف
class Base_Model(models.Model):
    # Field: Unique identifier for each model instance
    # فیلد: شناسه یکتا برای هر نمونه از مدل
    id = models.CharField(primary_key=True, default=generate_complex_id, max_length=10, editable=False)

    # Field: Date and time of creation
    # فیلد: تاریخ و زمان ایجاد
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ ایجاد',
                                      editable=False)

    # Field: Date and time of soft deletion
    # فیلد: تاریخ و زمان حذف نرم
    deleted_at = models.DateTimeField(default=None, null=True, blank=True, verbose_name='تاریخ حذف نرم')

    # Field: Flag indicating whether the instance is approved
    # فیلد: پرچم نشان‌دهنده تایید بودن نمونه
    is_ok = models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')

    # Field: Flag indicating whether the instance is changeable
    # فیلد: پرچم نشان‌دهنده تغییرپذیر بودن نمونه
    is_changeable = models.BooleanField(default=True, verbose_name='قابل تغییر است؟')

    class Meta:
        abstract = True  # Indicates that this class is an abstract class and should not create a table in the database

    def soft_delete(self):
        """
        تابع سافت‌دیلیت برای تنظیم تاریخ و زمان حذف به لحظه فراخوانی تابع
        """
        self.deleted_at = timezone.now()
        self.is_ok = False  # It might need to change this field as well
        self.is_changeable = False
        self.save()


# VerificationCode Model
# مدل VerificationCode

class VerificationCode(Base_Model):
    # Field for user association
    # فیلد ارتباطی با کاربر
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')

    # Field for a random code
    # فیلد برای کد تصادفی
    random_code = models.CharField(max_length=6, blank=True, null=True, verbose_name='کد تصادفی')

    # Field for creation time
    # فیلد برای زمان ایجاد
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    # Field for expiration time
    # فیلد برای زمان انقضاء
    expires_at = models.DateTimeField(verbose_name='تاریخ انقضاء')

    # Number of unsuccessful attempts
    # تعداد تلاش‌های ناموفق
    failed_attempts = models.IntegerField(default=0, verbose_name='تعداد تلاش‌های ناموفق')

    # Field indicating the validity status
    # فیلد نشان‌دهنده وضعیت اعتبار
    is_valid = models.BooleanField(default=True, auto_created=True, verbose_name='وضعیت اعتبار')

    # IP address field
    # فیلد آدرس IP
    ip = models.CharField(max_length=40, blank=True, null=True, verbose_name='آدرس IP')

    def __str__(self):
        # String representation of the VerificationCode
        # نمایش رشته‌ای از VerificationCode
        return f"{self.user} - {self.random_code} - {self.is_valid}"

    def save(self, *args, **kwargs):
        # Method to save VerificationCode with creation and expiration date settings
        # متد برای ذخیره کد اعتبارسنجی با تنظیمات تاریخ ایجاد و انقضاء
        if not self.created_at:
            self.created_at = timezone.now()

        # If the random code is not set, generate one
        # اگر کد تصادفی تنظیم نشده باشد، یکی تولید کنید
        if not self.random_code:
            self.random_code = random.randint(100000, 999999)

        # Set the expiration time to 3 minutes after creation time
        # تنظیم زمان انقضاء به مدت 3 دقیقه پس از زمان ایجاد
        self.expires_at = self.created_at + datetime.timedelta(minutes=3)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = 'کد های تایید'


# PasswordSetStatus Model
# مدل PasswordSetStatus

class PasswordSetStatus(Base_Model):
    # Field for Token association
    # فیلد ارتباطی با توکن
    token = models.OneToOneField(Token, on_delete=models.CASCADE, verbose_name='توکن')

    # Field indicating whether the password is set
    # فیلد نشان‌دهنده اینکه رمز عبور تنظیم شده است یا خیر
    is_password_set = models.BooleanField(default=False, verbose_name='آیا رمز عبور تنظیم شده است؟')

    class Meta:
        verbose_name = "وضعیت پسورد"
        verbose_name_plural = 'وضعیت پسورد کاربر ها'


# User Type List
# لیست انواع کاربر

type_user_list = (
    ("انتخاب نشده", "انتخاب نشده"),
    ("صاحب بار", "صاحب بار"),
    ("صاحب حمل کننده", "صاحب حمل کننده"),
    ("راننده", 'راننده'),
    ("ادمین", 'ادمین'),
)

# User Type Code Mapping
# نگاشت کد اختصاصی به نوع کاربر

type_user_code_mapping = {
    "صاحب بار": "CO",
    "صاحب حمل کننده": "CC",
    "راننده": "DR",
}


# In the Profile Model
# در مدل Profile

class Profile(Base_Model):
    # Field indicating whether the profile is completed
    # فیلد نشان‌دهنده اینکه پروفایل تکمیل شده است یا خیر
    is_completed = models.BooleanField(default=False, verbose_name="پروفایل تکمیل  شده؟")

    # Field indicating whether the profile is approved
    # فیلد نشان‌دهنده اینکه پروفایل تایید شده است یا خیر
    is_ok = models.BooleanField(default=False, verbose_name="پروفایل تایید شده؟")

    # Field for user association
    # فیلد ارتباطی با کاربر
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='کاربر', verbose_name='کاربر')

    # Field for user type
    # فیلد نوع کاربر
    user_type = models.CharField(max_length=255, default='انتخاب نشده', verbose_name="نوع کاربر",
                                 choices=type_user_list)

    wallet = models.FloatField(default=0, verbose_name='کیف پول', blank=True, null=True)

    # Field for a unique code
    # فیلد کد اختصاصی
    unique_code = models.CharField(max_length=25, verbose_name='کد اختصاصی', unique=True, help_text='کد اختصاصی')

    def save(self, *args, **kwargs):
        # Set the first letter based on the user type
        # تنظیم حرف اول بر اساس نوع کاربر
        code_prefix = type_user_code_mapping.get(self.user_type, "")

        # Generate a unique code if not already set or does not have the correct prefix
        # تولید کد اختصاصی اگر تنظیم نشده یا پیشوند صحیح نداشته باشد
        if len(self.unique_code) < 2 or self.unique_code is None or self.unique_code[:2] != code_prefix:
            self.unique_code = code_prefix + "-" + str(random.randint(1000, 9999))

        super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = 'پروفایل ها'


# GoodsOwner Model
# مدل صاحب بار

class GoodsOwner(Base_Model):
    # Field for user association
    # فیلد ارتباطی با کاربر
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='کاربر', verbose_name='کاربر')

    # Field for full name of the goods owner or CEO
    # فیلد نام کامل صاحب بار یا مدیر عامل
    full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی صاحب بار / مدیر عامل", blank=True,
                                 null=True)

    # Field for phone number of the goods owner or CEO
    # فیلد شماره موبایل صاحب بار یا مدیر عامل
    phone_number = models.CharField(max_length=15, verbose_name="موبایل صاحب بار / مدیر عامل", blank=True, null=True)

    # Field for national code or passport number of the goods owner or CEO
    # فیلد کد ملی یا شماره پاسپورت صاحب بار یا مدیر عامل
    national_code_passport_number = models.CharField(max_length=20, verbose_name="کد ملی / شماره پاسپورت", blank=True,
                                                     null=True)

    # Field for uploading the national card or passport image
    # فیلد آپلود تصویر کارت ملی یا پاسپورت
    national_card_passport_image = models.ImageField(upload_to='goods_owners/', blank=True, null=True,
                                                     verbose_name="آپلود کارت ملی / پاسپورت")

    # Field for the name of the company (if applicable)
    # فیلد نام شرکت (در صورت وجود)
    company_name = models.CharField(max_length=255, verbose_name="نام شرکت", blank=True, null=True)

    # Field for an optional national ID (if the owner does not have a company)
    # فیلد شناسه ملی اختیاری (در صورت عدم وجود شرکت)
    national_id_optional = models.CharField(max_length=20, verbose_name="شناسه ملی (اختیاری در صورت نداشتن شرکت)",
                                            blank=True, null=True)

    # Field for trade license expiry date
    # فیلد تاریخ انقضای کارت بازرگانی
    trade_license_expiry = models.DateField(verbose_name="کارت بازرگانی انقضا", blank=True, null=True)

    # Field for uploading the trade license image
    # فیلد آپلود تصویر کارت بازرگانی
    trade_license_image = models.ImageField(upload_to='goods_owners/', blank=True, null=True,
                                            verbose_name="آپلود کارت بازرگانی")

    # Field for the address of the goods owner or company
    # فیلد آدرس صاحب بار یا شرکت
    address = models.TextField(verbose_name="آدرس صاحب بار / شرکت", blank=True, null=True)

    # Field for the postal code of the goods owner or company
    # فیلد کدپستی صاحب بار یا شرکت
    postal_code = models.CharField(max_length=15, verbose_name="کدپستی صاحب بار / شرکت", blank=True, null=True)

    def __save__(self, *args, **kwargs):
        self.phone_number = self.user.username
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "صاحب بار"
        verbose_name_plural = "صاحبان بار"


# CarrierOwner Model
# مدل صاحب حمل‌کننده

class CarrierOwner(Base_Model):
    # Field for user association
    # فیلد ارتباطی با کاربر
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='کاربر', verbose_name='کاربر')

    # Field for uploading the car card image
    # فیلد آپلود تصویر کارت ماشین
    car_card_image = models.ImageField(upload_to='carriers/', blank=True, null=True, verbose_name="عکس کارت ماشین")

    # Field for uploading the insurance image
    # فیلد آپلود تصویر بیمه‌نامه
    insurance_image = models.ImageField(upload_to='carriers/', blank=True, null=True, verbose_name="عکس بیمه نامه")

    # Field for uploading the green sheet image
    # فیلد آپلود تصویر برگه سبز
    green_sheet_image = models.ImageField(upload_to='carriers/', blank=True, null=True, verbose_name="عکس برگه سبز")

    # Field for the national code or passport of the vehicle owner
    # فیلد کد ملی یا پاسپورت صاحب ماشین
    national_code_or_passport = models.CharField(max_length=20, null=True, blank=True,
                                                 verbose_name="کد ملی یا پاسپورت صاحب ماشین")

    # Field for uploading the national card image or passport
    # فیلد آپلود تصویر کارت ملی یا پاسپورت
    national_card_image = models.ImageField(upload_to='carriers/', blank=True, null=True,
                                            verbose_name="عکس کارت ملی یا پاسپورت")

    # Field for the full name of the vehicle owner
    # فیلد نام و نام خانوادگی صاحب ماشین
    owner_full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی صاحب ماشین", blank=True,
                                       null=True)

    # Field for the mobile number of the vehicle owner
    # فیلد شماره موبایل صاحب ماشین
    owner_mobile_number = models.CharField(max_length=15, verbose_name="شماره موبایل صاحب ماشین", blank=True, null=True)
    # فیلد نام شرکت حمل‌کننده
    company_name = models.CharField(max_length=255, verbose_name="نام شرکت حمل‌کننده", blank=True, null=True)

    # Field for the national ID of the carrier owner
    # فیلد شناسه ملی صاحب حمل‌کننده
    national_id = models.CharField(max_length=20, verbose_name="شناسه ملی صاحب حمل‌کننده", blank=True, null=True)

    # Field for the address of the carrier owner
    # فیلد آدرس صاحب حمل‌کننده
    address = models.TextField(verbose_name="آدرس", blank=True, null=True)

    # Field for the nationality of the carrier owner
    # فیلد ملیت صاحب حمل‌کننده
    nationality = models.CharField(max_length=50, verbose_name="ملیت", blank=True, null=True)

    # Field for selecting the legal status (individual or legal entity) of the carrier owner
    # فیلد انتخاب وضعیت حقوقی (حقیقی یا حقوقی) صاحب حمل‌کننده
    legal_status = models.CharField(max_length=20, verbose_name="وضعیت حقوقی", choices=(
        ("حقیقی", "حقیقی"),
        ("حقوقی", "حقوقی"),
    ), blank=True, null=True)

    def __save__(self, *args, **kwargs):
        self.owner_mobile_number = self.user.username

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "صاحب حمل‌کننده"
        verbose_name_plural = "صاحبان حمل‌کننده"


# Driver Model
# مدل راننده

class Driver(Base_Model):
    # Field: Flag indicating whether the instance is changeable
    # فیلد: پرچم نشان‌دهنده تغییرپذیر بودن نمونه
    is_changeable = models.BooleanField(default=False, verbose_name='قابل تغییر است؟')
    # Field for user association
    # فیلد ارتباطی با کاربر
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='کاربر', verbose_name='کاربر')

    # Field for the full name of the driver
    # فیلد نام و نام خانوادگی راننده
    driver_full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی راننده", blank=True, null=True)

    # Field for the national card or passport of the driver
    # فیلد کد ملی یا پاسپورت راننده
    national_card_or_passport = models.CharField(max_length=20, verbose_name="کد ملی یا پاسپورت راننده", blank=True,
                                                 null=True)

    # Field for uploading the national card image or passport
    # فیلد آپلود تصویر کارت ملی یا پاسپورت
    national_card_image = models.ImageField(upload_to='drivers/', blank=True, null=True,
                                            verbose_name="عکس کارت ملی یا پاسپورت")

    # Boolean field indicating the presence of the national card image
    # فیلد بولین برای نشان دادن وجود تصویر کارت ملی
    national_card_image_bool = models.BooleanField(default=False, verbose_name="عکس کارت ملی یا پاسپورت", blank=True,
                                                   null=True)

    # Field for the mobile number of the driver
    # فیلد شماره موبایل راننده
    mobile_number = models.CharField(max_length=15, verbose_name="شماره موبایل راننده", blank=True, null=True)

    # Field for the expiration date of the driver's license
    # فیلد تاریخ اعتبار گواهینامه راننده
    license_expiry_date = models.DateField(verbose_name="تاریخ اعتبار گواهینامه", blank=True, null=True)

    # Field for uploading the smart card image
    # فیلد آپلود تصویر کارت هوشمند
    smart_card_image = models.ImageField(upload_to='drivers/', blank=True, null=True, verbose_name="عکس کارت هوشمند")

    # Boolean field indicating the presence of the smart card image
    # فیلد بولین برای نشان دادن وجود تصویر کارت هوشمند
    smart_card_image_bool = models.BooleanField(default=False, verbose_name="عکس کارت هوشمند", blank=True, null=True)

    # Boolean field indicating the possession of a domestic license
    # فیلد بولین برای نشان دادن اختیار گواهی نامه داخلی
    domestic_license = models.BooleanField(default=False, verbose_name="گواهی نامه داخلی", blank=True, null=True)

    # Boolean field indicating the possession of an international license
    # فیلد بولین برای نشان دادن اختیار گواهینامه بین المللی
    international_license = models.BooleanField(default=False, verbose_name="گواهینامه بین المللی", blank=True,
                                                null=True)
    international_license_expiry_date = models.DateField(verbose_name="تاریخ اعتبار گواهینامه بین المللی", blank=True,
                                                         null=True)

    # Field for the city of the driver
    # فیلد شهر
    city = models.CharField(max_length=100, verbose_name="شهر", blank=True, null=True)

    # Field for the province of the driver
    # فیلد استان
    province = models.CharField(max_length=100, verbose_name="استان", blank=True, null=True)

    # ادرس
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='ادرس')
    # Field for uploading the health card image
    # فیلد آپلود تصویر کارت سلامت
    health_card_image = models.ImageField(upload_to='drivers/', blank=True, null=True, verbose_name="عکس کارت سلامت")

    # Field for the expiration date of the health card
    # فیلد تاریخ انقضا کارت سلامت
    health_card_expiry_date = models.DateField(verbose_name="تاریخ انقضا کارت سلامت", blank=True, null=True)
    type_of_cooperation = models.CharField(max_length=255, choices=(
        ('موقت', 'موقت'),
        ('دائم', 'دائم'),
        ('هردو', 'هردو'),
    ), blank=True, null=True, verbose_name='نوع همکاری')
    origin = models.CharField(verbose_name='مبدا راننده', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "راننده"
        verbose_name_plural = "رانندگان"

    def save(self, *args, **kwargs):
        # Set boolean fields based on the presence of images
        # تنظیم فیلدهای بولین بر اساس وجود تصاویر

        self.mobile_number = self.user.username
        if self.national_card_image != None:
            self.national_card_image_bool = True
        else:
            self.national_card_image_bool = False
        if self.smart_card_image != None:
            self.smart_card_image_bool = True
        else:
            self.smart_card_image_bool = False
        super().save(*args, **kwargs)
