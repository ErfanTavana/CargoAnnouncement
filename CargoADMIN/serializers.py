from rest_framework import serializers
from driver.models import Driver
from goods_owner.serializers import Base_ModelSerializer

class DriverSerializer(Base_ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'
