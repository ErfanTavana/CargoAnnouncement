from rest_framework import serializers
from goods_owner.serializers import Base_ModelSerializer
from .models import Captcha

class CaptchaSerializer(Base_ModelSerializer):
    class Meta:
        model = Captcha
        fields = (
            'id',
            'image',
            'guide',
        )
