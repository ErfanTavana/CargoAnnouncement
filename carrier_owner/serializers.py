from rest_framework import serializers
from .models import RoadFleet, CarOwReqDriver
from goods_owner.serializers import Base_ModelSerializer
from accounts.models import Driver, CarrierOwner, GoodsOwner
from goods_owner.models import RequiredCarrier, CommonCargo


class RoadFleetSerializer(Base_ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = Base_ModelSerializer.Meta.fields + (
            'user',
            'carrier_owner',
            'ownerType',
            'roomType',
            'vehichleType',
            'semiHeavyVehichle',
            'semiHeavyVehichleOthers',
            'HeavyVehichle',
            'heavy_vehicle_others',
            'plaque_one_num_check',
            'plaque_one_num',
            'plaque_puller_num_check',
            'plaque_puller_num',
            'plaque_carriage_num_check',
            'plaque_carriage_num',
            'plaque_container_num_check',
            'plaque_container_num',
            'vehicle_card',
            'vehicle_property_doc',
            'vehicle_advocate_date',
            'vehicle_advocate',
            'code_id',
            'owner_document',
            'international_docs',
            "carrier_type",
        )
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()
    # You can add additional validations or custom fields if needed


class DriverListCarrierOwner(Base_ModelSerializer):
    class Meta:
        model = Driver
        fields = Base_ModelSerializer.Meta.fields + (
            'id',
            'driver_full_name',
            'national_card_image_bool',
            'smart_card_image_bool',
            'domestic_license',
            'international_license',
            'city',
            'province',
        )
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


class RoadFleet_req_car_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = (
            'id', 'is_ok', 'ownerType', 'roomType', 'vehichleType', 'semiHeavyVehichle', 'semiHeavyVehichleOthers',
            'HeavyVehichle', 'heavy_vehicle_others', 'plaque_one_num_check', 'plaque_puller_num_check',
            'plaque_carriage_num_check', 'plaque_container_num_check', 'vehicle_card_bool',
            'vehicle_property_doc_bool', 'vehicle_advocate_date', 'international_docs_bool', 'carrier_type'
        )


class CarOwReqDriverSerializer(Base_ModelSerializer):
    carrier = RoadFleetSerializer()

    class Meta:
        model = CarOwReqDriver
        fields = Base_ModelSerializer.Meta.fields + (
            'user', 'carrier_owner', 'carrier', 'driver', 'collaboration_type', 'origin', 'destination',
            'proposed_price'
        )
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


from rest_framework import serializers
from goods_owner.models import RequiredCarrier, CommonCargo, InnerCargo, InternationalCargo

class InnerCargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnerCargo
        fields = [
            'id', 'length', 'width', 'height', 'cargoType', 'pkgType', 'description',
            'specialWidgets', 'storageBillNum', 'storagePrice', 'loadigPrice',
            'basculPrice', 'specialDesc', 'sendersName', 'sendersFamName',
            'dischargeTimeDate', 'duratio_ndischargeTime', 'country', 'state',
            'city', 'customName'
        ]

class RequiredCarrierSerializer(serializers.ModelSerializer):
    inner_cargo = InnerCargoSerializer(many=True, read_only=True)

    class Meta:
        model = RequiredCarrier
        fields = [
            'id', 'cargo_type', 'cargo_weight', 'counter', 'room_type', 'vehichle_type',
            'semi_heavy_vehichle', 'semi_heavy_vehichle_others', 'heavy_vehichle',
            'heavy_vehichle_others', 'special_widget_carrier', 'carrier_price',
            'cargo_price', 'relinquished', 'inner_cargo'
        ]

class InternationalCargoSerializer(serializers.ModelSerializer):
    carriers = RequiredCarrierSerializer(many=True, read_only=True)

    class Meta:
        model = InternationalCargo
        fields = [
            'id', 'length', 'width', 'height', 'cargoType', 'pkgType', 'description',
            'specialWidgets', 'storageBillNum', 'storagePrice', 'loadigPrice',
            'basculPrice', 'specialDesc', 'sendersName', 'sendersFamName',
            'dischargeTimeDate', 'duratio_ndischargeTime', 'country', 'state',
            'city', 'customName', 'carriers'
        ]
