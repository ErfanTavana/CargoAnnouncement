# General function purpose: This module configures the Django admin interface for the VerificationCode model.
# Admin Configuration for VerificationCode Model
# تنظیمات ادمین برای مدل VerificationCode

from django.contrib import admin
from .models import VerificationCode, Profile


@admin.register(VerificationCode)
class UserOTPAdmin(admin.ModelAdmin):
    # Displayed columns in the admin list view
    # ستون‌های نمایش داده شده در صفحه مدیریت

    list_display = ('user', 'random_code', 'created_at', 'expires_at', 'failed_attempts', 'is_valid')

    # Filters for narrowing down displayed results based on certain criteria
    # فیلترها برای محدود کردن نتایج نمایش داده شده بر اساس معیارهای خاص

    list_filter = ('is_valid',)  # Filter records based on their validity status

    # Search fields to enable searching for specific records
    # فیلدهای جستجو برای امکان جستجو برای رکوردهای خاص

    search_fields = (
    'user__username', 'user__email', 'otp')  # Search for records based on username, email, and otp fields

    # Editable field directly in the list view
    # فیلد قابل ویرایش به طور مستقیم در نمایش لیست

    list_editable = ('is_valid',)  # Allow editing the validity status directly in the list view


# Admin Configuration for PasswordSetStatus Model
# تنظیمات ادمین برای مدل PasswordSetStatus

from .models import PasswordSetStatus


class PasswordSetStatusAdmin(admin.ModelAdmin):
    list_display = ('token', 'is_password_set')  # Displayed fields in the list view
    # فیلدهایی که در لیست نمایش داده می‌شوند

    list_filter = ('is_password_set',)  # Filters available in the filter panel
    # فیلترهای موجود در پنل فیلتر

    search_fields = ('token__user__username',)  # Search based on the username of the user
    # جستجو بر اساس نام کاربری کاربر


admin.site.register(PasswordSetStatus, PasswordSetStatusAdmin)
# Admin Configuration for Profile Model
# تنظیمات ادمین برای مدل Profile

from django.contrib import admin
from .models import Profile

from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user_type', 'is_completed', 'is_ok', 'wallet', 'unique_code']
    list_filter = ['is_completed', 'is_ok']
    search_fields = ['user__username', 'unique_code']


admin.site.register(Profile, ProfileAdmin)
# Admin Configuration for Driver Model
# تنظیمات ادمین برای مدل Driver

from .models import Driver


class DriverAdmin(admin.ModelAdmin):
    list_display = (
    'driver_full_name', 'national_card_or_passport', 'mobile_number', 'license_expiry_date', 'domestic_license',
    'international_license')
    # Displayed fields in the list view
    # فیلدهایی که در لیست نمایش داده می‌شوند

    search_fields = ['driver_full_name', 'national_card_or_passport', 'mobile_number']
    # Search based on the specified fields
    # جستجو بر اساس فیلدهای مشخص شده

    list_filter = ('domestic_license', 'international_license')
    # Filters available in the filter panel
    # فیلترهای موجود در پنل فیلتر


admin.site.register(Driver, DriverAdmin)
# Admin Configuration for CarrierOwner Model
# تنظیمات ادمین برای مدل CarrierOwner

from .models import CarrierOwner


class CarrierAdmin(admin.ModelAdmin):
    list_display = ('owner_full_name', 'national_code_or_passport', 'owner_mobile_number')
    # Displayed fields in the list view
    # فیلدهایی که در لیست نمایش داده می‌شوند

    search_fields = ['owner_full_name', 'national_code_or_passport', 'owner_mobile_number']
    # Search based on the specified fields
    # جستجو بر اساس فیلدهای مشخص شده


admin.site.register(CarrierOwner, CarrierAdmin)
# Admin Configuration for GoodsOwner Model
# تنظیمات ادمین برای مدل GoodsOwner

from django.contrib import admin
from .models import GoodsOwner


@admin.register(GoodsOwner)
class GoodsOwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'is_changeable', 'phone_number', 'national_code_passport_number', 'company_name',
                    'trade_license_expiry')
    # Displayed fields in the list view
    # فیلدهایی که در لیست نمایش داده می‌شوند

    search_fields = ('full_name', 'phone_number', 'national_code_passport_number', 'company_name')
    # Search based on the specified fields
    # جستجو بر اساس فیلدهای مشخص شده

    list_filter = ('trade_license_expiry',)
    # Filter options available in the admin panel
    # گزینه‌های فیلتر موجود در پنل ادمین
