from django.contrib import admin
from .models import WagonDetails

class WagonDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'wagon_owner', 'owner_type', 'line_type', 'wagon_type', 'capacity', 'others', 'carrier_price', 'wagon_counts', 'wagon_nums')
    search_fields = ('user__username', 'wagon_owner__name', 'wagon_type', 'wagon_nums')

admin.site.register(WagonDetails, WagonDetailsAdmin)