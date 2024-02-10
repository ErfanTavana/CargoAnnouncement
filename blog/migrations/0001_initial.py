# Generated by Django 5.0.1 on 2024-02-10 13:27

import django.db.models.deletion
import goods_owner.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.CharField(default=goods_owner.models.generate_complex_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('image1', models.ImageField(upload_to='blog_images/', verbose_name='عکس 1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='blog_images/', verbose_name='عکس 2')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='موضوع')),
                ('category', models.CharField(blank=True, max_length=100, null=True, verbose_name='دسته بندی')),
                ('content', models.TextField(blank=True, null=True, verbose_name='متن')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
