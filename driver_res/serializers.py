from rest_framework import serializers
from goods_owner.serializers import Base_ModelSerializer
from carrier_owner.models import CarrierOwner, CarOwReqDriver, RoadFleet


# اطلاعات قابل نمایش صاحب حمل کننده برای راننده
class InfoCarrierOwnerResForDriverSerializers(Base_ModelSerializer):
    class Meta:
        model = CarrierOwner
        fields = (
            'owner_full_name',
        )


# اطلاعات قابل نمایش حمل کننده برای راننده
class InfoRoadFleetForDriverSerializers(Base_ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = (
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
            'international_docs_bool',
        )

# اطلاعات قابل نمایش یک درخواست برای راننده
class RequestsForDriverSerializers(Base_ModelSerializer):
    carrier_owner_full = InfoCarrierOwnerResForDriverSerializers(source='carrier_owner', read_only=True)
    carrier_full = InfoRoadFleetForDriverSerializers(source='carrier', read_only=True)

    class Meta:
        model = CarOwReqDriver
        fields = (
            'carrier_owner',
            'carrier_owner_full',
            'carrier',
            'carrier_full',
            'collaboration_type',
            'origin',
            'destination',
            'proposed_price',
            'request_result',
            'cancellation_time',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + (
            'request_result', 'cancellation_time', 'origin', 'destination', 'proposed_price', 'collaboration_type')
