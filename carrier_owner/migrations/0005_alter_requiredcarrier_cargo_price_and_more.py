# Generated by Django 5.0.1 on 2024-01-21 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrier_owner', '0004_alter_requiredcarrier_cargo_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requiredcarrier',
            name='cargo_price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='ارزش بار هر حمل کننده / خودرو'),
        ),
        migrations.AlterField(
            model_name='requiredcarrier',
            name='carrier_price',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='قیمت تقریبی حمل'),
        ),
        migrations.AlterField(
            model_name='requiredcarrier',
            name='heavy_vehichle_others',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='سایر'),
        ),
        migrations.AlterField(
            model_name='requiredcarrier',
            name='special_widget_carrier',
            field=models.TextField(blank=True, max_length=9999, null=True, verbose_name='ویژگی های خاص حمل کننده مورد نیاز'),
        ),
    ]
