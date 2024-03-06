from rest_framework import serializers
from goods_owner.models import InnerCargo, InternationalCargo, CommonCargo, Base_Model, \
    RequiredCarrier, CargoFleetCoordination, RailCargo, RequiredWagons, CargoWagonCoordination
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
            'specialDesc',
            'sendersName',
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
            'destination_area',
            'destination_custom_name',
            'is_bulk_cargo',
            'bulk_cargo_tonnage',
            'is_plannable',
            'weekly_days',
            'is_perishable',
            'refrigeration_temperature',
            'is_hazardous',
            'un_code',
            'customs_hs_code',
            'pallet_size',
            'pallet_size',
            'pallet_arrangement_type',
            'approximate_weight_per_packaging',
            'is_all_cargo_type',
            'approximate_weight_per_type',
            'specialized_lashing_required',
            'specialized_lashing_type_upload',
            'specialized_lashing_type_description',
            'need_warehouse',
            'warehouse_duration',
            'sender_additional_requests',
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
            'special_widget_carrier',
            'carrier_price',
            'cargo_price',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


class CargoFleetCoordinationSerializer(Base_ModelSerializer):
    class Meta:
        model = CargoFleetCoordination
        fields = Base_ModelSerializer.Meta.fields + (
            'inner_cargo',
            'international_cargo',
            'required_carrier',
            'road_fleet',
            'status_result',
        )


class RailCargoSerializer(Base_ModelSerializer):
    class Meta:
        model = RailCargo
        fields = (
            'approval_status',
            'rejection_reason',
            'id',
            'user',
            'goods_owner',
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialDesc',
            'sendersName',
            'senderMobileNum',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'delivery_provider_name',
            'delivery_provider_national_id',
            'delivery_provider_full_name',
            'delivery_provider_mobile',
            'cargo_receiver_name',
            'cargo_receiver_national_id',
            'cargo_receiver_full_name',
            'cargo_receiver_mobile',
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
            'destination_area',
            'destination_custom_name',
            'is_bulk_cargo',
            'bulk_cargo_tonnage',
            'is_plannable',
            'weekly_days',
            'is_perishable',
            'refrigeration_temperature',
            'is_hazardous',
            'un_code',
            'customs_hs_code',
            'pallet_size',
            'pallet_arrangement_type',
            'approximate_weight_per_packaging',
            'is_all_cargo_type',
            'approximate_weight_per_type',
            'specialized_lashing_required',
            'specialized_lashing_type_upload',
            'specialized_lashing_type_description',
            'need_warehouse',
            'warehouse_duration',
            'sender_additional_requests',
            'cargo_procedure_type',
            'need_route_code',
            'route_code',
        )
        read_only_fields = (
            'approval_status',
            'rejection_reason',
        )


class RequiredWagonsSerializer(Base_ModelSerializer):
    class Meta:
        model = RequiredWagons
        fields = (
            'id',
            'user',
            'goods_owner',
            'cargo_type',
            'rail_cargo',
            'wagon_type',
            'capacity',
            'net_weight',
            'counter',
        )


class CargoWagonCoordinationSerializer(Base_ModelSerializer):
    class Meta:
        model = CargoWagonCoordination
        fields = (
            'id',
            'rail_cargo',
            'required_wagons',
            'wagon_owner',
            'status_result',
        )
