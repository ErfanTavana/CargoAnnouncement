# General function purpose: This module defines a Django model for VerificationCode, which is associated with a User model.

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


# Abstract base class for common fields among different models
class Base_Model(models.Model):
    id = models.CharField(primary_key=True, default=generate_complex_id, max_length=10, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ ایجاد')
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
        self.is_changeable = False
        self.save()


class VerificationCode(Base_Model):
    # Field for user association
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)  # ForeignKey to associate the VerificationCode with a User model

    # Field for a random code
    random_code = models.CharField(max_length=6, blank=True, null=True)  # Field to store a random 6-digit code

    # Field for creation time
    created_at = models.DateTimeField(auto_now_add=True)  # AutoField to store the creation time of the VerificationCode

    # Field for expiration time
    expires_at = models.DateTimeField()  # Field to store the expiration time of the VerificationCode

    # Number of unsuccessful attempts
    failed_attempts = models.IntegerField(default=0)  # Field to store the number of unsuccessful attempts

    # Field indicating the validity status
    is_valid = models.BooleanField(default=True,
                                   auto_created=True)  # BooleanField to indicate the validity status of the VerificationCode

    # IP address field
    ip = models.CharField(max_length=40, blank=True,
                          null=True)  # Field to store the IP address associated with the VerificationCode

    def __str__(self):
        return f"{self.user} - {self.random_code} - {self.is_valid}"  # String representation of the VerificationCode

    # Method to save VerificationCode with creation and expiration date settings
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()  # Set the creation time to the current time if not already set

        # If the random code is not set, generate one
        if not self.random_code:
            self.random_code = random.randint(100000, 999999)  # Generate a random 6-digit code if not already set
        # Set the expiration time to 3 minutes after creation time
        self.expires_at = self.created_at + datetime.timedelta(
            minutes=2)  # Set the expiration time to 3 minutes after creation time

        super().save(*args, **kwargs)  # Call the save method of the parent class


class PasswordSetStatus(Base_Model):
    token = models.OneToOneField(Token, on_delete=models.CASCADE)
    is_password_set = models.BooleanField(default=False)


type_user_list = (
    ("انتخاب نشده", "انتخاب نشده"),
    ("صاحب بار", "صاحب بار"),
    ("صاحب حمل کننده", "صاحب حمل کننده"),
    ("راننده", 'راننده'),
)

type_user_code_mapping = {
    "صاحب بار": "CO",
    "صاحب حمل کننده": "CC",
    "راننده": "DR",
}


# در مدل Profile
class Profile(Base_Model):
    is_completed = models.BooleanField(default=False, verbose_name="پروفایل تکمیل  شده؟")
    is_ok = models.BooleanField(default=False, verbose_name="پروفایل تایید شده؟")
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='کاربر', verbose_name='کاربر')
    user_type = models.CharField(max_length=255, default='انتخاب نشده', verbose_name="نوع کاربر",
                                 choices=type_user_list)
    unique_code = models.CharField(max_length=25, verbose_name='کد اختصاصی', unique=True, help_text='کد اختصاصی')

    def save(self, *args, **kwargs):
        # تنظیم حرف اول بر اساس نوع کاربر
        code_prefix = type_user_code_mapping.get(self.user_type, "")
        if len(self.unique_code) < 2 or self.unique_code == None or self.unique_code[:2] != code_prefix:
            self.unique_code = code_prefix + "-" + str(random.randint(1000, 9999))
        super(Profile, self).save(*args, **kwargs)


class GoodsOwner(Base_Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='کاربر', verbose_name='کاربر')
    full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی صاحب بار / مدیر عامل", blank=True,
                                 null=True)
    phone_number = models.CharField(max_length=15, verbose_name="موبایل صاحب بار / مدیر عامل", blank=True, null=True)
    national_code_passport_number = models.CharField(max_length=20, verbose_name="کد ملی / شماره پاسپورت", blank=True,
                                                     null=True)
    national_card_passport_image = models.ImageField(upload_to='goods_owners/', blank=True, null=True,
                                                     verbose_name="آپلود کارت ملی / پاسپورت")
    company_name = models.CharField(max_length=255, verbose_name="نام شرکت", blank=True, null=True)
    national_id_optional = models.CharField(max_length=20, verbose_name="شناسه ملی (اختیاری در صورت نداشتن شرکت)",
                                            blank=True, null=True)
    trade_license_expiry = models.DateField(verbose_name="کارت بازرگانی انقضا", blank=True, null=True)
    trade_license_image = models.ImageField(upload_to='goods_owners/', blank=True, null=True,
                                            verbose_name="آپلود کارت بازرگانی")
    address = models.TextField(verbose_name="آدرس صاحب بار / شرکت", blank=True, null=True)
    postal_code = models.CharField(max_length=15, verbose_name="کدپستی صاحب بار / شرکت", blank=True, null=True)

    class Meta:
        verbose_name = "صاحب بار"
        verbose_name_plural = "صاحبان بار"


class CarrierOwner(Base_Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='کاربر', verbose_name='کاربر')
    car_card_image = models.ImageField(upload_to='carriers/', blank=True, null=True, verbose_name="عکس کارت ماشین")
    insurance_image = models.ImageField(upload_to='carriers/', blank=True, null=True, verbose_name="عکس بیمه نامه")
    green_sheet_image = models.ImageField(upload_to='carriers/', blank=True, null=True, verbose_name="عکس برگه سبز")
    national_code_or_passport = models.CharField(max_length=20, verbose_name="کد ملی یا پاسپورت صاحب ماشین")
    national_card_image = models.ImageField(upload_to='carriers/', blank=True, null=True,
                                            verbose_name="عکس کارت ملی یا پاسپورت")
    owner_full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی صاحب ماشین", blank=True,
                                       null=True)
    owner_mobile_number = models.CharField(max_length=15, verbose_name="شماره موبایل صاحب ماشین", blank=True, null=True)

    class Meta:
        verbose_name = "صاحب حمل‌کننده"
        verbose_name_plural = " صاحبان حمل کننده ها"


class Driver(Base_Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='کاربر', verbose_name='کاربر')

    driver_full_name = models.CharField(max_length=255, verbose_name="نام و نام خانوادگی راننده", blank=True, null=True)
    national_card_or_passport = models.CharField(max_length=20, verbose_name="کد ملی یا پاسپورت راننده", blank=True,
                                                 null=True)
    national_card_image = models.ImageField(upload_to='drivers/', blank=True, null=True,
                                            verbose_name="عکس کارت ملی یا پاسپورت")
    national_card_image_bool = models.BooleanField(default=False, verbose_name="عکس کارت ملی یا پاسپورت", blank=True,
                                                   null=True)
    mobile_number = models.CharField(max_length=15, verbose_name="شماره موبایل راننده", blank=True, null=True)
    license_expiry_date = models.DateField(verbose_name="تاریخ اعتبار گواهینامه", blank=True, null=True)
    smart_card_image = models.ImageField(upload_to='drivers/', blank=True, null=True, verbose_name="عکس کارت هوشمند")
    smart_card_image_bool = models.BooleanField(default=False, verbose_name="عکس کارت هوشمند", blank=True, null=True)
    domestic_license = models.BooleanField(default=False, verbose_name="گواهی نامه داخلی", blank=True, null=True)
    international_license = models.BooleanField(default=False, verbose_name="گواهینامه بین المللی", blank=True,
                                                null=True)
    # فیلد شهر
    city = models.CharField(max_length=100, verbose_name="شهر", blank=True, null=True)
    # فیلد استان
    province = models.CharField(max_length=100, verbose_name="استان", blank=True, null=True)

    class Meta:
        verbose_name = "راننده"
        verbose_name_plural = "رانندگان"

    def save(self, *args, **kwargs):
        if self.national_card_image != None:
            self.national_card_image_bool = True
        else:
            self.national_card_image_bool = False
        if self.smart_card_image != None:
            self.smart_card_image_bool = True
        else:
            self.smart_card_image_bool = False
        super().save(*args, **kwargs)
