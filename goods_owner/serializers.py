from rest_framework import serializers
from goods_owner.models import InnerCargo, InternationalCargo, CommonCargo, Base_Model, RequiredCarrier
from django.contrib.auth.models import User
from accounts.serializers import GoodsOwnerSerializer

# سریالایزر برای مدل پایه
class Base_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base_Model
        # فیلدهای مدل پایه که در سریالایزر قابل دسترسی هستند
        fields = (
            'id',
            'created_at',
            'deleted_at',
            'is_ok',
            'is_changeable',
            'is_deletable',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = (
            'id',
            'created_at',
            'deleted_at',
            'is_ok',
            'is_changeable',
            'is_deletable',
        )


# سریالایزر برای مدل مشترک بار
class CommonCargoSerializer(Base_ModelSerializer):
    class Meta(Base_ModelSerializer.Meta):
        model = CommonCargo
        # فیلدهای مدل پایه و فیلدهای اضافی مدل مشترک بار در سریالایزر
        fields = Base_ModelSerializer.Meta.fields + (
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
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


# سریالایزر برای مدل بار داخلی
class InnerCargoSerializer(CommonCargoSerializer):
    class Meta(CommonCargoSerializer.Meta):
        model = InnerCargo
        # ارث‌بری از سریالایزر مشترک بار و اضافه کردن فیلد تاریخ و ساعت تحویل بار در مدل بار داخلی
        fields = CommonCargoSerializer.Meta.fields + (
            'deliveryTimeDate',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


# سریالایزر برای مدل بار خارجی
class InternationalCargoSerializer(Base_ModelSerializer):
    class Meta(Base_ModelSerializer.Meta):
        model = InternationalCargo
        # ارث‌بری از سریالایزر پایه و اضافه کردن فیلدهای مختلف برای مدل بار خارجی
        fields = CommonCargoSerializer.Meta.fields + (
            'senderCountry',
            'senderState',
            'senderCity',
            'senderStreet',
            'senderAddress',
            'deliveryTimeDate',
            'dischargeTimeDate',
            'dischargeTime',
            'customNameEnd',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()


class RequiredCarrierSerializer(Base_ModelSerializer):
    class Meta:
        model = RequiredCarrier
        fields = Base_ModelSerializer.Meta.fields + (
            'cargo_type',
            'user',
            'inner_cargo',
            'international_cargo',
            'cargo_weight',
            'counter',
            'room_type',
            'vehichle_type',
            'semi_heavy_vehichle',
            'semi_heavy_vehichle_others',
            'heavy_vehichle',
            'heavy_vehichle_others',
            'special_widget_carrier',
            'carrier_price',
            'cargo_price',
        )
        # تنظیم فیلدهای فقط خواندنی در سریالایزر
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + ()
