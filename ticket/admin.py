# در فایل admin.py در داخل اپلیکیشن tickets
from django.contrib import admin
from .models import Tickets

class TicketsAdmin(admin.ModelAdmin):
    list_display = ['issue', 'full_name', 'account_type', 'importance_level', 'phone_number', 'email', 'additional_comments']
    search_fields = ['issue', 'full_name', 'phone_number', 'email']

admin.site.register(Tickets, TicketsAdmin)