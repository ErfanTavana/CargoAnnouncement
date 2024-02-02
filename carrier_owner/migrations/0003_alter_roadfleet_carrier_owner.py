# Generated by Django 5.0.1 on 2024-02-02 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('carrier_owner', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadfleet',
            name='carrier_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.carrierowner', verbose_name='صاحب حمل کننده'),
        ),
    ]