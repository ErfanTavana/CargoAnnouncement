from rest_framework import serializers
from .models import HomePageInfo
from blog.models import Blog
from goods_owner.serializers import Base_ModelSerializer


class HomePageInfoSerializers(Base_ModelSerializer):
    class Meta:
        model = HomePageInfo
        fields = Base_ModelSerializer.Meta.fields + (
            'ready_to_work_drivers',
            'distance_covered',
            'loads_carried',
            'country',
            'province',
            'city',
            'address',
            'full_address',
            'phone_prefix',
            'phone_number',
            'email',
            'working_days',
            'telegram_address',
            'whatsapp_address',
            'instagram_address',
            'facebook_address',
            'android_app',
            'web_app_address',
            'whatsapp_mz',
            'linkedin_mz',
            'instagram_mz',
            'telegram_mz',
            'vichat_mz',
        )


class BlogSerializers(Base_ModelSerializer):
    class Meta:
        model = Blog
        fields = Base_ModelSerializer.Meta.fields + (
            'image1',
            'image2',
            'title',
            'category',
            'content',
        )
