from rest_framework import serializers
from goods_owner.serializers import Base_ModelSerializer
from .models import Captcha

# from django.views import View
from django.http import HttpResponse
# current_domain = request.META.get('HTTP_HOST', None)
class CaptchaSerializer(Base_ModelSerializer):
    class Meta:
        model = Captcha
        fields = (
            'id',
            'image',
            'guide',
        )
