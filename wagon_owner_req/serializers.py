from goods_owner.serializers import Base_ModelSerializer
from .models import SentCollaborationRequestToRailCargo


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
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + (
            'request_result',
        )

