from django.contrib import admin
from .models import SentCollaborationRequestToGoodsOwner

class SentCollaborationRequestToGoodsOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'carrier_owner', 'road_fleet', 'goods_owner', 'required_carrier',
                    'cargo_fleet_coordination', 'proposed_price', 'request_result')
    search_fields = ('user__username', 'carrier_owner__name', 'goods_owner__user__username')
    list_filter = ('request_result',)

admin.site.register(SentCollaborationRequestToGoodsOwner, SentCollaborationRequestToGoodsOwnerAdmin)
################################################################
# ارسال درخواست همکاری به راننده
