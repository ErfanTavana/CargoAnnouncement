from goods_owner.serializers import Base_ModelSerializer
from .models import WalletTransaction


class WalletTransactionSerializer(Base_ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = (
            'created_at',
            'user',
            'amount',
            'is_increase',
            'reason',
        )
