from .models import Blog
from goods_owner.serializers import Base_ModelSerializer


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
        read_only_fields = Base_ModelSerializer.Meta.read_only_fields + (
            'image1',
            'image2',
            'title',
            'category',
            'content',
        )
