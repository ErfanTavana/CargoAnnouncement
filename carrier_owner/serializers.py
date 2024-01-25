from rest_framework import serializers
from .models import RoadFleet, Base_Model
from goods_owner.serializers import Base_ModelSerializer


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
    # You can add additional validations or custom fields if needed
