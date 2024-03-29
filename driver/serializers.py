from rest_framework import serializers
from .models import DriverReqCarrierOwner
from accounts.models import CarrierOwner
from goods_owner.serializers import Base_ModelSerializer


class CarrierOwnerForDriverSerializers(Base_ModelSerializer):
    class Meta:
        model = CarrierOwner
        fields = (
            'id',
            'owner_full_name',
        )


class DriverReqCarrierOwnerSerializer(Base_ModelSerializer):
    carrier_owner_full = CarrierOwnerForDriverSerializers(source='carrier_owner', read_only=True)

    class Meta:
        model = DriverReqCarrierOwner
        fields = Base_ModelSerializer.Meta.fields + (
            'id',
            'user',
            'driver',
            'carrier_owner',
            'carrier_owner_full',
            'cargo_type',
            'proposed_price',
            'request_result',
            'cancellation_time',
            'source',
            'destination',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()
