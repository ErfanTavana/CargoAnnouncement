# Generated by Django 5.0.1 on 2024-02-02 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods_owner', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodsownerreqcarow',
            name='required_carrier',
        ),
    ]