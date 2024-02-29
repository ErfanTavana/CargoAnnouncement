# serializers.py
from rest_framework import serializers
from .models import SentCollaborationRequestToGoodsOwner
from goods_owner.serializers import Base_ModelSerializer


class SentCollaborationRequestToGoodsOwnerSerializer(Base_ModelSerializer):
    class Meta:
        model = SentCollaborationRequestToGoodsOwner
        fields = (
            'user',
            'carrier_owner',
            'road_fleet',
            'goods_owner',
            'required_carrier',
            'cargo_fleet_coordination',
            'proposed_price',
        )
