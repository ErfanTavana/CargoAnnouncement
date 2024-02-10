from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')  # فیلدهایی که در لیست نمایش داده می‌شوند
    search_fields = ['title', 'category']  # فیلدهایی که قابل جستجو هستند

admin.site.register(Blog, BlogAdmin)