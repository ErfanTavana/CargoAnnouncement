# serializers.py
from rest_framework import serializers
from .models import Profile, GoodsOwner, Driver, CarrierOwner
import random


# Serializer Class: GoodsOwnerSerializer
# کلاس سریال‌ساز: GoodsOwnerSerializer
class GoodsOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsOwner
        fields = ["full_name", 'phone_number', 'national_code_passport_number', 'national_card_passport_image',
                  'company_name', 'national_id_optional', 'trade_license_expiry', 'trade_license_image', 'address',
                  'postal_code']


class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrierOwner
        fields = ['car_card_image',
                  'insurance_image',
                  'green_sheet_image',
                  'national_code_or_passport',
                  'national_card_image',
                  'owner_full_name',
                  'owner_mobile_number',
                  'company_name',
                  'national_id',
                  'address',
                  'nationality',
                  'legal_status',

                  ]


from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('driver_full_name', 'national_card_or_passport', 'national_card_image',
                  'mobile_number', 'license_expiry_date', 'smart_card_image', 'domestic_license',
                  'international_license', 'city', 'province', 'international_license_expiry_date', 'address',
                  'health_card_image', 'health_card_expiry_date', 'type_of_cooperation', 'origin',
                  'cooperate_with_carrier_owners', 'is_changeable',)
