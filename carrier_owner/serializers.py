from rest_framework import serializers
from .models import RoadFleet, CarOwReqDriver
from goods_owner.serializers import Base_ModelSerializer
from accounts.models import Driver, CarrierOwner, GoodsOwner
from goods_owner.models import RequiredCarrier, CommonCargo
from goods_owner.models import  InnerCargo,InternationalCargo

# سریالایزر برای مدل RoadFleet
# نام سریالایزر: RoadFleetSerializer
class RoadFleetSerializer(Base_ModelSerializer):
    class Meta:
        model = RoadFleet
        # فیلدهای مدل و مدل پایه را در اینجا مشخص کنید
        fields = Base_ModelSerializer.Meta.fields + (
            'user',
            'carrier_owner',
            'ownerType',
            'driver',
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
        # فیلدهای تنها خواندنی را اگر وجود دارد اینجا مشخص کنید
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()
    # اگر نیاز به اعتبارسنجی یا اضافه کردن فیلدهای سفارشی دارید، می‌توانید در اینجا انجام دهید


# سریالایزر برای مدل Driver به عنوان لیست رانندگان مربوط به صاحب حمل کننده
# نام سریالایزر: DriverListCarrierOwner
class DriverListCarrierOwner(Base_ModelSerializer):
    class Meta:
        model = Driver
        # فیلدهای مدل و مدل پایه را در اینجا مشخص کنید
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
        # فیلدهای تنها خواندنی را اگر وجود دارد اینجا مشخص کنید
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


# سریالایزر برای مدل RoadFleet به عنوان درخواست حمل‌ونقل از راننده برای صاحب حمل کننده
# نام سریالایزر: RoadFleet_req_car_Serializer
class RoadFleet_req_car_Serializer(serializers.ModelSerializer):
    class Meta:
        model = RoadFleet
        # فیلدهای مدل و مدل پایه را در اینجا مشخص کنید
        fields = (
            'id', 'is_ok', 'ownerType', 'roomType', 'vehichleType', 'semiHeavyVehichle', 'semiHeavyVehichleOthers',
            'HeavyVehichle', 'heavy_vehicle_others', 'plaque_one_num_check', 'plaque_puller_num_check',
            'plaque_carriage_num_check', 'plaque_container_num_check', 'vehicle_card_bool',
            'vehicle_property_doc_bool', 'vehicle_advocate_date', 'international_docs_bool', 'carrier_type'
        )
        # فیلدهای تنها خواندنی را اگر وجود دارد اینجا مشخص کنید
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


# سریالایزر برای مدل CarOwReqDriver به عنوان درخواست حمل‌ونقل از صاحب حمل کننده به راننده
# نام سریالایزر: CarOwReqDriverSerializer
class CarOwReqDriverSerializer(Base_ModelSerializer):
    # اضافه کردن سریالایزر RoadFleetSerializer به عنوان فیلد 'carrier'

    class Meta:
        model = CarOwReqDriver
        # فیلدهای مدل و مدل پایه را در اینجا مشخص کنید
        fields = Base_ModelSerializer.Meta.fields + (
            'user', 'request_result', 'carrier_owner', 'carrier', 'driver', 'collaboration_type', 'origin',
            'destination',
            'proposed_price'
        )
        # فیلدهای تنها خواندنی را اگر وجود دارد اینجا مشخص کنید
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()

from rest_framework import serializers

# سریالایزر برای مدل RoadFleet
class RoadFleet2Serializer(serializers.ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = [
            'ownerType',
            'roomType',
            'vehichleType',
            'semiHeavyVehichle',
            'semiHeavyVehichleOthers',
            'HeavyVehichle',
            'heavy_vehicle_others',
            'plaque_one_num_check',
            'plaque_puller_num_check',
            'plaque_carriage_num_check',
            'plaque_container_num_check',
            'vehicle_card_bool',
            'vehicle_property_doc_bool',
            'vehicle_advocate_bool',
        ]

# سریالایزر برای مدل InnerCargo
class InnerCargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnerCargo
        fields = [
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
            'sendersFamName',
            'specialDesc',
            'dischargeTimeDate',
            'country',
            'state',
            'city',
            'customName',
            'deliveryTimeDate',
        ]

# سریالایزر برای مدل InternationalCargo
class InternationalCargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalCargo
        fields = [
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
            'sendersFamName',
            'specialDesc',
            'dischargeTimeDate',
            'duration_dischargeTime',
            'country',
            'state',
            'city',
            'customName',
            'senderCountry',
            'senderState',
            'senderStreet',
            'deliveryTimeDate',
            'dischargeTime',
            'customNameEnd',
        ]

# سریالایزر برای مدل RequiredCarrier
class RequiredCarrierSerializer(serializers.ModelSerializer):
    inner_cargo = InnerCargoSerializer()
    international_cargo = InternationalCargoSerializer()

    class Meta:
        model = RequiredCarrier
        fields = [
            'relinquished',
            'cargo_type',
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
        ]