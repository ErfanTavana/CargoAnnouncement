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
    list_filter = ('cargo_type', 'room_type', 'vehichle_type', 'is_ok')
    search_fields = ('id', 'cargo_type', 'room_type', 'vehichle_type')


from django.contrib import admin
from .models import CargoFleetCoordination


class CargoFleetCoordinationAdmin(admin.ModelAdmin):
    list_display = ['id', 'inner_cargo', 'international_cargo', 'required_carrier', 'road_fleet', 'status_result']
    list_filter = ['status_result']
    search_fields = ['inner_cargo__id', 'international_cargo__id', 'required_carrier__id', 'road_fleet__id']


admin.site.register(CargoFleetCoordination, CargoFleetCoordinationAdmin)
# your_app/admin.py

from django.contrib import admin
from .models import RailCargo


class RailCargoAdmin(admin.ModelAdmin):
    list_display = ('user', 'goods_owner', 'length', 'width', 'height', 'cargoType', 'pkgType', 'description')
    search_fields = ['user__username', 'goods_owner__user__username', 'cargoType', 'pkgType']
    list_filter = ('cargoType', 'pkgType', 'is_bulk_cargo', 'is_plannable', 'is_perishable', 'is_hazardous')
    ordering = ('-created_at',)  # Replace 'created_at' with the actual field you want to use for sorting


# Register the RailCargo model with the custom admin class
admin.site.register(RailCargo, RailCargoAdmin)

from django.contrib import admin
from .models import CargoWagonCoordination

from django.contrib import admin
from .models import RequiredWagons


class RequiredWagonsAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'user', 'goods_owner', 'relinquished', 'cargo_type', 'rail_cargo', 'wagon_type', 'capacity', 'net_weight',
    'counter')
    list_filter = ('relinquished', 'cargo_type', 'wagon_type', 'capacity')
    search_fields = (
    'user__username', 'goods_owner__name', 'rail_cargo__name')  # مواردی که قابل جستجو در پنل ادمین باشند


admin.site.register(RequiredWagons, RequiredWagonsAdmin)


class CargoWagonCoordinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'rail_cargo', 'required_wagons', 'wagon_owner', 'status_result')
    list_filter = ('status_result',)
    search_fields = ('rail_cargo__name', 'wagon_owner__name')  # مواردی که قابل جستجو در پنل ادمین باشند


admin.site.register(CargoWagonCoordination, CargoWagonCoordinationAdmin)
