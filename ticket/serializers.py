from goods_owner.serializers import Base_ModelSerializer
from .models import Tickets


class TicketsSerializers(Base_ModelSerializer):
    class Meta:
        model = Tickets
        fields = Base_ModelSerializer.Meta.fields + (
            'issue',
            'full_name',
            'account_type',
            'importance_level',
            'phone_number',
            'email',
            'additional_comments',
        )
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()