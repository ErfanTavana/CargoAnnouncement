from django.contrib import admin

from django.contrib import admin
from .models import Captcha

class CaptchaAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'expires_at', 'is_valid']
    search_fields = ['id', 'created_at', 'expires_at', 'is_valid']
    list_filter = ['is_valid']

admin.site.register(Captcha, CaptchaAdmin)