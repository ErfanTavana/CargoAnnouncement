from rest_framework import serializers
from goods_owner.models import InnerCargo, GoodsOwnerReqCarOw, InternationalCargo, CommonCargo, Base_Model, \
    RequiredCarrier, CargoDeclaration
from django.contrib.auth.models import User
from accounts.serializers import GoodsOwnerSerializer
from carrier_owner.models import RoadFleet, CarrierOwner


# سریالایزر برای مدل پایه
class Base_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base_Model
        # فیلدهای مدل پایه که در سریالایزر قابل دسترسی هستند
        fields = (
            'id',
            'created_at',
            'deleted_at',
            'is_ok',
            'is_changeable',
            'is_deletable',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = (
            'id',
            'created_at',
            'deleted_at',
            'is_ok',
            'is_changeable',
            'is_deletable',
        )


# سریالایزر برای مدل مشترک بار
class CommonCargoSerializer(Base_ModelSerializer):
    class Meta(Base_ModelSerializer.Meta):
        model = CommonCargo
        # فیلدهای مدل پایه و فیلدهای اضافی مدل مشترک بار در سریالایزر
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
            'cargo_receiver_surname',
            'destination_country',
            'destination_state',
            'destination_city',
            'destination_street',
            'destination_address',
            'destination_custom_name',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


# سریالایزر برای مدل بار داخلی
class InnerCargoSerializer(CommonCargoSerializer):
    class Meta(CommonCargoSerializer.Meta):
        model = InnerCargo
        # ارث‌بری از سریالایزر مشترک بار و اضافه کردن فیلد تاریخ و ساعت تحویل بار در مدل بار داخلی
        fields = CommonCargoSerializer.Meta.fields + (
            'deliveryTimeDate',
            'dischargeTimeDate',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


# سریالایزر برای مدل بار خارجی
class InternationalCargoSerializer(Base_ModelSerializer):
    class Meta(Base_ModelSerializer.Meta):
        model = InternationalCargo
        # ارث‌بری از سریالایزر پایه و اضافه کردن فیلدهای مختلف برای مدل بار خارجی
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
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


class RequiredCarrierSerializer(Base_ModelSerializer):
    class Meta:
        model = RequiredCarrier
        fields = Base_ModelSerializer.Meta.fields + (
            'cargo_type',
            'user',
            'goods_owner',
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
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


# نمایش اطلاعات صاحب  حمل کننده
class CarrierOwnerForGoodsOwnerSerializer(Base_ModelSerializer):
    class Meta:
        model = CarrierOwner
        fields = ['owner_full_name']
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


# Serializer for displaying information about a RoadFleet related to goods owners
class RoadFleetForGoodsOwnerSerializer(Base_ModelSerializer):
    carrier_owner = CarrierOwnerForGoodsOwnerSerializer()

    class Meta:
        model = RoadFleet
        fields = Base_ModelSerializer.Meta.fields + (
            'ownerType',
            'carrier_owner',
            'roomType',
            'vehichleType',
            'semiHeavyVehichle',
            'semiHeavyVehichleOthers',
            'HeavyVehichle',
            'heavy_vehicle_others',
            'vehicle_card_bool',
            'vehicle_property_doc_bool',
            'vehicle_advocate_bool',
            'international_docs_bool',
            'carrier_type',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


# درخواست همکاری صاحب بار به صاحب حمل کننده
class GoodsOwnerReqCarOwSerializer(Base_ModelSerializer):
    # carrier_owner = CarrierOwnerForGoodsOwnerSerializer()
    class Meta:
        model = GoodsOwnerReqCarOw
        fields = Base_ModelSerializer.Meta.fields + (
            'id',
            'user',
            'goods_owner',
            'inner_cargo',
            'international_cargo',
            'carrier_owner',
            'proposed_price',
            'request_result',
            'cancellation_time',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


class CargoDeclarationSerializer(Base_ModelSerializer):
    class Meta:
        model = CargoDeclaration
        fields = (
            'id',
            'user',
            'goods_owner',
            'relinquished',
            'cargo_type',
            'inner_cargo',
            'international_cargo',
            'net_weight',
            'special_features',
            'approximate_transport_price',
            'value_per_wagon',
            'wagon_type',
            'route_code',
            'station_code',
            'is_plannable',
            'tonnage_per_shift',
            'is_partial_cargo',
            'tonnage',
            'cargo_type',

        )
