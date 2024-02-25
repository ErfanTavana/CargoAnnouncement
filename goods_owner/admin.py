from django.contrib import admin
from .models import Base_Model, InternationalCargo, InnerCargo


class InnerCargoAdmin(admin.ModelAdmin):
    list_display = ['user', 'length', 'width', 'height', 'cargoType', 'pkgType', 'description', 'specialWidgets',
                    'specialDesc', 'sendersName',
                    'senderMobileNum', 'dischargeTimeDate', 'duratio_ndischargeTime', 'user',
                    'country', 'state', 'city', 'street', 'address', 'customName', 'deliveryTimeDate']
    search_fields = ['cargoType', 'user__username', 'country']
    list_filter = ['pkgType', 'specialWidgets']
    date_hierarchy = 'dischargeTimeDate'


# Register the InnerCargo model with the custom admin class
admin.site.register(InnerCargo, InnerCargoAdmin)


# Define a custom admin class for the InternationalCargo model
class InternationalCargoAdmin(admin.ModelAdmin):
    list_display = ['user', 'length', 'width', 'height', 'cargoType', 'pkgType', 'description', 'specialWidgets',
                    'specialDesc', 'sendersName',
                    'senderMobileNum', 'dischargeTimeDate', 'duratio_ndischargeTime', 'user',
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
    list_display = ('id', "relinquished", 'cargo_type', 'cargo_weight', 'counter', 'room_type', 'vehichle_type',
                     'special_widget_carrier', 'carrier_price',
                    'cargo_price', 'created_at', 'deleted_at', 'is_ok', 'is_changeable')
    list_filter = ('cargo_type', 'room_type', 'vehichle_type',   'is_ok')
    search_fields = ('id', 'cargo_type', 'room_type', 'vehichle_type')


from django.contrib import admin
from .models import CargoFleetCoordination


class CargoFleetCoordinationAdmin(admin.ModelAdmin):
    list_display = ['id', 'inner_cargo', 'international_cargo', 'required_carrier', 'road_fleet', 'status_result']
    list_filter = ['status_result']
    search_fields = ['inner_cargo__id', 'international_cargo__id', 'required_carrier__id', 'road_fleet__id']


admin.site.register(CargoFleetCoordination, CargoFleetCoordinationAdmin)
from django.contrib import admin
from .models import GoodsOwnerReqCarOw


class GoodsOwnerReqCarOwAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'goods_owner', 'carrier_owner', 'proposed_price', 'request_result', 'cancellation_time')
    list_filter = ('request_result', 'cancellation_time')
    search_fields = ('user__username', 'goods_owner__name', 'carrier_owner__name')
    readonly_fields = ('id',)


admin.site.register(GoodsOwnerReqCarOw, GoodsOwnerReqCarOwAdmin)
# your_app/admin.py

from django.contrib import admin
from .models import CargoDeclaration


class CargoDeclarationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cargo_type', 'relinquished', 'is_partial_cargo')
    list_filter = ('cargo_type', 'relinquished', 'is_partial_cargo')
    search_fields = ('id', 'user__username', 'route_code')


admin.site.register(CargoDeclaration, CargoDeclarationAdmin)
