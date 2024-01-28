# Generated by Django 5.0.1 on 2024-01-27 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_carrierowner_is_ok_alter_driver_is_ok_and_more'),
        ('carrier_owner', '0008_alter_roadfleet_international_docs_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carowreqdriver',
            name='goods_owner',
        ),
        migrations.AddField(
            model_name='carowreqdriver',
            name='carrier_owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.carrierowner', verbose_name='صاحب حمل کننده'),
            preserve_default=False,
        ),
    ]