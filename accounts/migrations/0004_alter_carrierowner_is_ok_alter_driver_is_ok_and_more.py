# Generated by Django 5.0.1 on 2024-01-27 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_driver_national_card_image_bool_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrierowner',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
        migrations.AlterField(
            model_name='goodsowner',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
        migrations.AlterField(
            model_name='passwordsetstatus',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
        migrations.AlterField(
            model_name='verificationcode',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
    ]
