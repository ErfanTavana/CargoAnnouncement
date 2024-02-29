from rest_framework import serializers
from goods_owner.serializers import Base_ModelSerializer
from carrier_owner.models import CarrierOwner, RoadFleet
from driver.models import DriverReqCarrierOwner


# اطلاعات قابل نمایش صاحب حمل کننده برای راننده
class InfoCarrierOwnerResForDriverSerializers(Base_ModelSerializer):
    class Meta:
        model = CarrierOwner
        fields = (
            'id',
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
            # 'plaque_one_num_check',
            # 'plaque_puller_num_check',
            # 'plaque_carriage_num_check',
            # 'plaque_container_num_check',
            'vehicle_card_bool',
            'vehicle_property_doc_bool',
            'vehicle_advocate_bool',
            'international_docs_bool',
            'carrier_type',
        )

class SentDriverReqSerializers(Base_ModelSerializer):
    carrier_owner_full = InfoCarrierOwnerResForDriverSerializers(source='carrier_owner', read_only=True)

    class Meta:
        model = DriverReqCarrierOwner
        fields = Base_ModelSerializer.Meta.fields + (
            'driver',  # اینجا ویرگول افزوده شده است
            'carrier_owner',
            'carrier_owner_full',
            'cargo_type',
            'proposed_price',
            'request_result',
            'cancellation_time',
            'source',
            'destination',
        )