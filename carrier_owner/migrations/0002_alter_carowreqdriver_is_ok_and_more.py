# Generated by Django 5.0.1 on 2024-01-30 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrier_owner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carowreqdriver',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
        migrations.AlterField(
            model_name='carowreqgoodsowner',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
        migrations.AlterField(
            model_name='roadfleet',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
    ]