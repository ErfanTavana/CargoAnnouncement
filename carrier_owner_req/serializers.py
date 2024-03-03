# serializers.py
from rest_framework import serializers
from .models import SentCollaborationRequestToGoodsOwner, SentCollaborationRequestToDriver
from goods_owner.serializers import Base_ModelSerializer
from goods_owner.models import CargoFleetCoordination, InnerCargo, InternationalCargo, RequiredCarrier
from carrier_owner.models import RoadFleet
from carrier_owner.serializers import RoadFleetSerializer
from accounts.models import Driver


class InfoInnerCargoSerializer(Base_ModelSerializer):
    class Meta:
        model = InnerCargo
        fields = (
            #################
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialWidgets',
            'specialDesc',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'country',
            'state',
            'city',
            'street',
            'customName',
            'destination_country',
            'destination_state',
            'destination_city',
            'destination_street',
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
            'route_code',
            ##########################
            'deliveryTimeDate',
            'dischargeTimeDate',
        )


class InternationalCargoSerializer(Base_ModelSerializer):
    class Meta:
        model = InternationalCargo
        fields = (
            #################
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialWidgets',
            'specialDesc',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'country',
            'state',
            'city',
            'street',
            'customName',
            'destination_country',
            'destination_state',
            'destination_city',
            'destination_street',
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
            'route_code',
            ##########################
            'senderCountry',
            'senderState',
            'senderCity',
            'senderStreet',
            'deliveryTimeDate',
            'dischargeTimeDate',
            'dischargeTime',
            'customNameEnd',
            'cargo_weight',
        )


class InfoRequiredCarrierSerializer(Base_ModelSerializer):
    class Meta:
        model = RequiredCarrier
        fields = (
            'cargo_type',
            'inner_cargo',
            'international_cargo',
            'cargo_weight',
            'counter',
            'room_type',
            'vehichle_type',
            'special_widget_carrier',
            'carrier_price',
            'cargo_price',
        )


class InfoRoadFleetSerializer(Base_ModelSerializer):
    class Meta:
        model = RoadFleet
        fields = (
            'ownerType',
            'roomType',
            'vehichleType',
            'vehichleTypeOthers',
            'semiHeavyVehichle',
            'semiHeavyVehichleOthers',
            'HeavyVehichle',
            'heavy_vehicle_others',
            'vehicle_card_bool',
            'vehicle_property_doc_bool',
            'vehicle_advocate_bool',
            'international_docs_bool',
        )


class CargoFleetCoordinationSerializer(Base_ModelSerializer):
    inner_cargo_full = InfoInnerCargoSerializer(source='inner_cargo', read_only=True)
    international_cargo_full = InternationalCargoSerializer(source='international_cargo', read_only=True)
    required_carrier_full = InfoRequiredCarrierSerializer(source='required_carrier', read_only=True)
    road_fleet_full = InfoRoadFleetSerializer(source='road_fleet', read_only=True)

    class Meta:
        model = CargoFleetCoordination
        fields = (
            'id',
            'inner_cargo',
            'inner_cargo_full',
            'international_cargo',
            'international_cargo_full',
            'required_carrier',
            'required_carrier_full',
            'road_fleet',
            'road_fleet_full',
            'status_result',
        )


class SentCollaborationRequestToGoodsOwnerSerializer(Base_ModelSerializer):
    road_fleet_full = InfoRoadFleetSerializer(source='road_fleet', read_only=True)
    cargo_fleet_coordination_full = CargoFleetCoordinationSerializer(source='cargo_fleet_coordination', read_only=True)

    class Meta:
        model = SentCollaborationRequestToGoodsOwner
        fields = (
            'id',
            'user',
            'carrier_owner',
            'road_fleet',
            'road_fleet_full',
            'goods_owner',
            'required_carrier',
            'cargo_fleet_coordination',
            'cargo_fleet_coordination_full',
            'proposed_price',
            'request_result',
        )


################################################################
# ارسال درخواست همکاری به راننده

class InfoDriverSerializer(Base_ModelSerializer):
    class Meta:
        model = Driver
        fields = (
            'id',
            'national_card_image_bool',
            'license_expiry_date',
            'smart_card_image_bool',
            'domestic_license',
            'international_license',
            'international_license_expiry_date',
            'city',
            'province',
            'health_card_expiry_date',
            'type_of_cooperation',
            'origin',
            'cooperate_with_carrier_owners',
        )


class SentCollaborationRequestToDriverSerializer(Base_ModelSerializer):
    road_fleet_full = RoadFleetSerializer(source='road_fleet', read_only=True)

    class Meta:
        model = SentCollaborationRequestToDriver
        fields = (
            'id',
            'user',
            'carrier_owner',
            'road_fleet',
            'road_fleet_full',
            'driver',
            'request_type',
            'source_location',
            'destination_location',
            'proposed_price',
            'request_result',
            'estimated_loading_time_at_source',
            'estimated_delivery_time_at_destination',
        )
