from django.contrib import admin
from .models import RoadFleet, CarOwReqDriver


class RoadFleetAdmin(admin.ModelAdmin):
    list_display = ('user', 'carrier_owner', 'ownerType', 'roomType', 'vehichleType', 'carrier_type')
    search_fields = (
        'user__username', 'user__email', 'carrier_owner__user__username', 'ownerType', 'roomType', 'vehichleType',
        'carrier_type')
    list_filter = ('ownerType', 'roomType', 'vehichleType', 'carrier_type')


admin.site.register(RoadFleet, RoadFleetAdmin)


# درخواست همکاری صاحب حمل کننده از راننده
# CarrierOwnerReqquestDriver
@admin.register(CarOwReqDriver)
class CarOwReqDriverAdmin(admin.ModelAdmin):
    list_display = (
        'carrier_owner', 'request_result', 'carrier', 'driver', 'collaboration_type', 'origin', 'destination',
        'proposed_price')
    search_fields = ('goods_owner__full_name', 'carrier_owner__full_name', 'driver__driver_full_name')
    list_filter = ('collaboration_type', 'origin', 'destination')


from .models import CarOwReqGoodsOwner


@admin.register(CarOwReqGoodsOwner)
class CarOwReqGoodsOwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'carrier_owner', 'road_fleet', 'goods_owner', 'required_carrier', 'proposed_price',
                    'request_result']
    search_fields = ['user__username', 'goods_owner__name']  # جستجو بر اساس نام کاربری و نام صاحب بار
    list_filter = ['request_result', 'road_fleet']  # فیلتر کردن بر اساس نتیجه درخواست و حمل کننده
