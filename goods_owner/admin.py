from django.contrib import admin
from .models import Base_Model, InternationalCargo, InnerCargo


class InnerCargoAdmin(admin.ModelAdmin):
    list_display = ['user', 'length', 'width', 'height', 'cargoType', 'pkgType', 'description', 'specialWidgets',
                    'storageBillNum', 'storagePrice', 'loadigPrice', 'basculPrice', 'specialDesc', 'sendersName',
                    'sendersFamName', 'senderMobileNum', 'dischargeTimeDate', 'duratio_ndischargeTime', 'user',
                    'country', 'state', 'city', 'street', 'address', 'customName', 'deliveryTimeDate']
    search_fields = ['cargoType', 'user__username', 'country']
    list_filter = ['pkgType', 'specialWidgets']
    date_hierarchy = 'dischargeTimeDate'


# Register the InnerCargo model with the custom admin class
admin.site.register(InnerCargo, InnerCargoAdmin)


# Define a custom admin class for the InternationalCargo model
class InternationalCargoAdmin(admin.ModelAdmin):
    list_display = ['user', 'length', 'width', 'height', 'cargoType', 'pkgType', 'description', 'specialWidgets',
                    'storageBillNum', 'storagePrice', 'loadigPrice', 'basculPrice', 'specialDesc', 'sendersName',
                    'sendersFamName', 'senderMobileNum', 'dischargeTimeDate', 'duratio_ndischargeTime', 'user',
                    'country', 'state', 'city', 'street', 'address', 'customName', 'deliveryTimeDate', 'senderCountry',
                    'senderState', 'senderCity', 'senderStreet', 'senderAddress', 'customNameEnd']
    search_fields = ['cargoType', 'user__username', 'country', 'senderCountry']
    list_filter = ['pkgType', 'specialWidgets']
    date_hierarchy = 'dischargeTimeDate'


# Register the InternationalCargo model with the custom admin class
admin.site.register(InternationalCargo, InternationalCargoAdmin)

from .models import RequiredCarrier


@admin.register(RequiredCarrier)
class RequiredCarrierAdmin(admin.ModelAdmin):
    list_display = ('id', "relinquished",'cargo_type', 'cargo_weight', 'counter', 'room_type', 'vehichle_type',
                    'semi_heavy_vehichle', 'heavy_vehichle', 'special_widget_carrier', 'carrier_price',
                    'cargo_price', 'created_at', 'deleted_at', 'is_ok', 'is_changeable')
    list_filter = ('cargo_type', 'room_type', 'vehichle_type', 'semi_heavy_vehichle', 'heavy_vehichle', 'is_ok')
    search_fields = ('id', 'cargo_type', 'room_type', 'vehichle_type', 'semi_heavy_vehichle', 'heavy_vehichle')