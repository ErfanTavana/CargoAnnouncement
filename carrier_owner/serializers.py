from rest_framework import serializers
from carrier_owner.models import InnerCargo, InternationalCargo, CommonCargo, Base_Model


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
        fields = Base_ModelSerializer.Meta.fields + (
            'sender_country',
            'sender_state',
            'sender_city',
            'sender_street',
            'sender_address',
            'delivery_time_date',
            'discharge_time_date_destination',
            'discharge_time_destination',
            'custom_name_destination',
        )
