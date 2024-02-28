from django.contrib import admin
from .models import SentCollaborationRequestToRailCargo

class SentCollaborationRequestToRailCargoAdmin(admin.ModelAdmin):
    list_display = ('user', 'wagon_owner', 'wagon_details', 'rail_cargo', 'required_wagons', 'proposed_price', 'created_at')
    search_fields = ('user__username', 'wagon_owner__user__username', 'rail_cargo__your_field_name_here')
    list_filter = ('created_at',)

admin.site.register(SentCollaborationRequestToRailCargo, SentCollaborationRequestToRailCargoAdmin)
from django.contrib import admin

# Register your models here.
