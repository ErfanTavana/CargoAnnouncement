from rest_framework import serializers
from .models import RoadFleet
from goods_owner.serializers import Base_ModelSerializer

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

# سریالایزر برای مدل RoadFleet
class RoadFleet2Serializer(serializers.ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = [
            'id',
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