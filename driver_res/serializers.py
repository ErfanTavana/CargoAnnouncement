from goods_owner.serializers import Base_ModelSerializer
from carrier_owner_req.models import SentCollaborationRequestToDriver
from carrier_owner_req.models import RoadFleet


class InfoRoadFleetSerializer(Base_ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = (
            'roomType',
            'vehichleType',
            'vehicle_card_bool',
            'vehicle_property_doc_bool',
            'vehicle_advocate_date',
            'vehicle_advocate_bool',
            'international_docs_bool',
            'carrier_type',
        )


class InfoSentCollaborationRequestToDriverSerializer(Base_ModelSerializer):
    road_fleet_full = InfoRoadFleetSerializer(source="road_fleet", read_only=True)

    class Meta:
        model = SentCollaborationRequestToDriver
        fields = (
            'id',
            'road_fleet',
            'road_fleet_full',
            'request_type',
            'source_location',
            'destination_location',
            'proposed_price',
            'request_result',
            'estimated_loading_time_at_source',
            'estimated_delivery_time_at_destination',
        )
