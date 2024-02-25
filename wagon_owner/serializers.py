from rest_framework import serializers
from goods_owner.serializers import Base_ModelSerializer
from .models import WagonDetails
from accounts.serializers import WagonOwnerSerializer


class WagonDetailsSerializer(Base_ModelSerializer):
    wagon_owner_full = WagonOwnerSerializer(source='wagon_owner', many=False,read_only=True)

    class Meta:
        model = WagonDetails
        fields = (
            'id',
            'user',
            'wagon_owner',
            'wagon_owner_full',
            'owner_type',
            'line_type',
            'wagon_type',
            'capacity',
            'others',
            'wagon_docs',
            'carrier_price',
            'wagon_counts',
            'wagon_nums',
        )
