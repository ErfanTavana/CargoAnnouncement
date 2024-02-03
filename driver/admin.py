from django.contrib import admin
from .models import DriverReqCarrierOwner


class DriverReqCarrierOwnerAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'driver', 'carrier_owner', 'cargo_type', 'proposed_price', 'request_result', 'cancellation_time', 'source',
    'destination')
    list_filter = ('cargo_type', 'request_result')
    search_fields = ('user__username', 'driver__name', 'carrier_owner__name', 'source', 'destination')
    readonly_fields = ('cancellation_time',)


admin.site.register(DriverReqCarrierOwner, DriverReqCarrierOwnerAdmin)
