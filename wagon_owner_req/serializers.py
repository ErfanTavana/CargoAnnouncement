from goods_owner.serializers import Base_ModelSerializer
from .models import SentCollaborationRequestToRailCargo
from goods_owner.models import CargoWagonCoordination, RailCargo
from .models import RequiredWagons


class InfoRailCargoShowSerializer(Base_ModelSerializer):
    class Meta:
        model = RailCargo
        fields = (
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialDesc',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'country',
            'state',
            'city',
            'street',
            'address',
            'customName',
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
        )


class InfoRequiredWagonsShowSerializer(Base_ModelSerializer):
    class Meta:
        model = RequiredWagons
        fields = (
            'cargo_type',
            'wagon_type',
            'capacity',
            'net_weight',
        )


class InfoCargoWagonCoordinationShowSerializer(Base_ModelSerializer):
    rail_cargo_full = InfoRailCargoShowSerializer(source='rail_cargo', read_only=True)
    required_wagons_full = InfoRequiredWagonsShowSerializer(source='required_wagons', read_only=True)

    class Meta:
        model = CargoWagonCoordination
        fields = (
            'id',
            'rail_cargo',
            'rail_cargo_full',
            'required_wagons',
            'required_wagons_full',
            'wagon_owner',
            'status_result',
        )


class SentCollaborationRequestToRailCargoSerializer(Base_ModelSerializer):
    class Meta:
        model = SentCollaborationRequestToRailCargo
        fields = (
            'user',
            'wagon_owner',
            'wagon_details',
            'rail_cargo',
            'required_wagons',
            'proposed_price',
            'cargo_wagon_coordination',
            'request_result'
        )
