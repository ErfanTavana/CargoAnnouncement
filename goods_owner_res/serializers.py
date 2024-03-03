from goods_owner.serializers import Base_ModelSerializer
from wagon_owner_req.models import SentCollaborationRequestToRailCargo
from wagon_owner.models import WagonDetails
from goods_owner.models import RailCargo
#####
from carrier_owner_req.models import SentCollaborationRequestToGoodsOwner
from carrier_owner.models import RoadFleet


##########
# اطلاعات درخواست همکاری
class InfoWagonDetailsSerializer(Base_ModelSerializer):
    class Meta:
        model = WagonDetails
        fields = (
            'id',
            'owner_type',
            'line_type',
            'wagon_type',
            'capacity',
            'others',
            'carrier_price',
            'wagon_counts',
            'wagon_nums',
        )


from goods_owner.serializers import RailCargoSerializer
from goods_owner.serializers import RequiredWagonsSerializer


class RequestReceivedFromTheWagonOwnerSerializer(Base_ModelSerializer):
    wagon_details_full = InfoWagonDetailsSerializer(source='wagon_details', read_only=True)
    rail_cargo_full = RailCargoSerializer(source='rail_cargo', read_only=True)
    required_wagons_full = RequiredWagonsSerializer(source='required_wagons', read_only=True)

    class Meta:
        model = SentCollaborationRequestToRailCargo
        fields = (
            'id',
            'wagon_details',
            'wagon_details_full',
            'rail_cargo',
            'rail_cargo_full',
            'required_wagons',
            'required_wagons_full',
            'cargo_wagon_coordination',
            'proposed_price',
            'request_result',
        )


#############################
class InfoRoadFleetSerializer(Base_ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = (
            'id',
            'ownerType',
            'roomType',
            'vehichleType',
            'vehicle_card_bool',
            'vehicle_property_doc_bool',
            'vehicle_advocate_bool',
            'vehicle_advocate_date',
            'vehicle_advocate_bool',
            'international_docs_bool',
            'carrier_type',
        )


from goods_owner.serializers import RequiredCarrierSerializer


class RequestReceivedFromTheCarrierOwnerSerializer(Base_ModelSerializer):
    road_fleet_full = InfoRoadFleetSerializer(source="road_fleet", read_only=True)
    required_carrier_full = RequiredCarrierSerializer(source='required_carrier', read_only=True)

    class Meta:
        model = SentCollaborationRequestToGoodsOwner
        fields = (
            'id',
            'road_fleet',
            'road_fleet_full',
            'required_carrier',
            'required_carrier_full',
            'proposed_price',
            'request_result',
        )
