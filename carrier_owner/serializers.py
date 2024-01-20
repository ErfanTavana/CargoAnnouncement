from rest_framework import serializers
from carrier_owner.models import InnerCargo


class InnerCargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnerCargo
        fields = (
            'id',
            'created_at',
            # 'deleted_at',
            # 'is_ok',
            # 'is_changeable',
            'user',
            'goods_owner',
            'length',
            'width',
            'height',
            'cargoType',
            'pkgType',
            'description',
            'specialWidgets',
            'storageBillNum',
            'storagePrice',
            'loadigPrice',
            'basculPrice',
            'specialDesc',
            'sendersName',
            'sendersFamName',
            'senderMobileNum',
            'dischargeTimeDate',
            'duratio_ndischargeTime',
            'country',
            'state',
            'city',
            'street',
            'address',
            'customName',
            'deliveryTimeDate',
        )
