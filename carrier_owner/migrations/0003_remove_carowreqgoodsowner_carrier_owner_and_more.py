# Generated by Django 5.0.1 on 2024-03-01 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrier_owner', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carowreqgoodsowner',
            name='carrier_owner',
        ),
        migrations.RemoveField(
            model_name='carowreqgoodsowner',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='carowreqgoodsowner',
            name='goods_owner',
        ),
        migrations.RemoveField(
            model_name='carowreqgoodsowner',
            name='required_carrier',
        ),
        migrations.RemoveField(
            model_name='carowreqgoodsowner',
            name='road_fleet',
        ),
        migrations.RemoveField(
            model_name='carowreqgoodsowner',
            name='user',
        ),
        migrations.DeleteModel(
            name='CarOwReqDriver',
        ),
        migrations.DeleteModel(
            name='CarOwReqGoodsOwner',
        ),
    ]
