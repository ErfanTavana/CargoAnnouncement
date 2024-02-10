from django.db import models
from goods_owner.models import Base_Model
class Blog(Base_Model):
    image1 = models.ImageField(upload_to='blog_images/', verbose_name='عکس 1')
    image2 = models.ImageField(upload_to='blog_images/', verbose_name='عکس 2', blank=True, null=True)
    title = models.CharField(max_length=200, verbose_name='موضوع',blank=True,null=True)
    category = models.CharField(max_length=100, verbose_name='دسته بندی',blank=True,null=True)
    content = models.TextField(verbose_name='متن',blank=True,null=True)
    def __str__(self):
        return self.title