# General function purpose: This module configures the Django admin interface for the VerificationCode model.

from django.contrib import admin
from .models import VerificationCode ,Profile

@admin.register(VerificationCode)
class UserOTPAdmin(admin.ModelAdmin):
    # Displayed columns in the admin list view
    list_display = ('user', 'random_code', 'created_at', 'expires_at', 'failed_attempts', 'is_valid')

    # Filters for narrowing down displayed results based on certain criteria
    list_filter = ('is_valid',)  # Filter records based on their validity status

    # Search fields to enable searching for specific records
    search_fields = ('user__username', 'user__email', 'otp')  # Search for records based on username, email, and otp fields

    # Editable field directly in the list view
    list_editable = ('is_valid',)  # Allow editing the validity status directly in the list view

    # Number of items to display per page
    list_per_page = 20  # Set the number of items to display per page in the admin list view



from .models import PasswordSetStatus

class PasswordSetStatusAdmin(admin.ModelAdmin):
    list_display = ('token', 'is_password_set')  # فیلدهایی که در لیست نمایش داده می‌شوند
    list_filter = ('is_password_set',)  # فیلترهای موجود در پنل فیلتر
    search_fields = ('token__user__username',)  # جستجو بر اساس نام کاربری کاربر

admin.site.register(PasswordSetStatus, PasswordSetStatusAdmin)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_ok', 'user_type', 'unique_code')
    list_filter = ('is_ok', 'user_type')
    search_fields = ('user__username', 'unique_code')

admin.site.register(Profile, ProfileAdmin)

from django.contrib import admin
from .models import Driver

class DriverAdmin(admin.ModelAdmin):
    list_display = ('driver_full_name', 'national_card_or_passport', 'mobile_number', 'license_expiry_date', 'domestic_license', 'international_license')
    search_fields = ['driver_full_name', 'national_card_or_passport', 'mobile_number']
    list_filter = ('domestic_license', 'international_license')

admin.site.register(Driver, DriverAdmin)
from django.contrib import admin
from .models import CarrierOwner

class CarrierAdmin(admin.ModelAdmin):
    list_display = ('owner_full_name', 'national_code_or_passport', 'owner_mobile_number')
    search_fields = ['owner_full_name', 'national_code_or_passport', 'owner_mobile_number']

admin.site.register(CarrierOwner, CarrierAdmin)
from django.contrib import admin
from .models import GoodsOwner

@admin.register(GoodsOwner)
class GoodsOwnerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'national_code_passport_number', 'company_name', 'trade_license_expiry')
    search_fields = ('full_name', 'phone_number', 'national_code_passport_number', 'company_name')
    list_filter = ('trade_license_expiry',)
