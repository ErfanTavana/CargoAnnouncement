from rest_framework import serializers
from .models import RoadFleet, CarOwReqDriver
from goods_owner.serializers import Base_ModelSerializer
from accounts.models import Driver, CarrierOwner, GoodsOwner
from goods_owner.models import RequiredCarrier, CommonCargo
from .models import CarOwReqGoodsOwner


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
    carrier = RoadFleetSerializer()

    class Meta:
        model = CarOwReqDriver
        # فیلدهای مدل و مدل پایه را در اینجا مشخص کنید
        fields = Base_ModelSerializer.Meta.fields + (
            'user', 'request_result', 'carrier_owner', 'carrier', 'driver', 'collaboration_type', 'origin',
            'destination',
            'proposed_price'
        )
        # فیلدهای تنها خواندنی را اگر وجود دارد اینجا مشخص کنید
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ('request_result',)


# سریالایزر برای مدل CarOwReqGoodsOwner به عنوان درخواست حمل‌ونقل از صاحب حمل کننده به صاحب بار
# نام سریالایزر: CarOwReqGoodsOwnerSerializer
class CarOwReqGoodsOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarOwReqGoodsOwner
        # فیلدهای مدل و مدل پایه را در اینجا مشخص کنید
        fields = [
            'user',
            'carrier_owner',
            'road_fleet',
            'goods_owner',
            'required_carrier',
            'proposed_price',
            'request_result',
        ]
        # فیلدهای تنها خواندنی را اگر وجود دارد اینجا مشخص کنید
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()
