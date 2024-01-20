# serializers.py
from rest_framework import serializers
from .models import Profile, GoodsOwner, Driver, CarrierOwner
import random


class GoodsOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsOwner
        fields = ["full_name",'phone_number','national_code_passport_number','national_card_passport_image','company_name','national_id_optional','trade_license_expiry','trade_license_image','address','postal_code']

class CarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrierOwner
        fields = ['car_card_image', 'insurance_image', 'green_sheet_image',
                  'national_code_or_passport', 'national_card_image', 'owner_full_name', 'owner_mobile_number']


from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('driver_full_name', 'national_card_or_passport', 'national_card_image',
                  'mobile_number', 'license_expiry_date', 'smart_card_image', 'domestic_license',
                  'international_license')
