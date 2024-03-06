from rest_framework import serializers
from goods_owner.serializers import Base_ModelSerializer

from goods_owner.models import RailCargo


class InfoRailCargoSerializer(Base_ModelSerializer):
    class Meta:
        model = RailCargo
        fields = (
            'id',
            'approval_status',
            'rejection_reason',
            'id',
            'user',
            'goods_owner',
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialDesc',
            'sendersName',
            'senderMobileNum',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'delivery_provider_name',
            'delivery_provider_national_id',
            'delivery_provider_full_name',
            'delivery_provider_mobile',
            'cargo_receiver_name',
            'cargo_receiver_national_id',
            'cargo_receiver_full_name',
            'cargo_receiver_mobile',
            'country',
            'state',
            'city',
            'street',
            'address',
            'customName',
            'cargo_receiver_surname',
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
            'route_code',
        )