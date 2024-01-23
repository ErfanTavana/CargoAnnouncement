from rest_framework import serializers
from carrier_owner.models import InnerCargo, InternationalCargo, CommonCargo, Base_Model,RequiredCarrier


class Base_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base_Model
        fields = (
            'id',
            'created_at',
            'deleted_at',
            'is_ok',
            'is_changeable',
        )
        read_only_fields = (
            'id',
            'created_at',
            'deleted_at',
            'is_ok',
            'is_changeable',
        )


class CommonCargoSerializer(Base_ModelSerializer):
    class Meta(Base_ModelSerializer.Meta):
        model = CommonCargo
        fields = Base_ModelSerializer.Meta.fields + (
            'user',
            'goods_owner',
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialWidgets',
            'storageBillNum',
            'storagePrice',
            'loadigPrice',
            'basculPrice',
            'specialDesc',
            'sendersName',
            'sendersFamName',
            'senderMobileNum',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'country',
            'state',
            'city',
            'street',
            'address',
            'customName',
        )


class InnerCargoSerializer(CommonCargoSerializer):
    class Meta(CommonCargoSerializer.Meta):
        model = InnerCargo
        fields = CommonCargoSerializer.Meta.fields + (
            'deliveryTimeDate',
        )


class InternationalCargoSerializer(Base_ModelSerializer):
    class Meta(Base_ModelSerializer.Meta):
        model = InternationalCargo
        fields = CommonCargoSerializer.Meta.fields + (
            'senderCountry',
            'senderState',
            'senderCity',
            'senderStreet',
            'senderAddress',
            'deliveryTimeDate',
            'dischargeTimeDate',
            'dischargeTime',
            'customNameEnd',
        )


class RequiredCarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredCarrier
        fields = (
            'cargo_type',
            'user',
            'inner_cargo',
            'international_cargo',
            'cargo_weight',
            'counter',
            'room_type',
            'vehichle_type',
            'semi_heavy_vehichle',
            'semi_heavy_vehichle_others',
            'heavy_vehichle',
            'heavy_vehichle_others',
            'special_widget_carrier',
            'carrier_price',
            'cargo_price',
        )
