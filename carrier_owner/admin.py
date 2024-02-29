from django.contrib import admin
from .models import RoadFleet


class RoadFleetAdmin(admin.ModelAdmin):
    list_display = ('user', 'carrier_owner', 'ownerType', 'roomType', 'vehichleType', 'carrier_type')
    search_fields = (
        'user__username', 'user__email', 'carrier_owner__user__username', 'ownerType', 'roomType', 'vehichleType',
        'carrier_type')
    list_filter = ('ownerType', 'roomType', 'vehichleType', 'carrier_type')


admin.site.register(RoadFleet, RoadFleetAdmin)

