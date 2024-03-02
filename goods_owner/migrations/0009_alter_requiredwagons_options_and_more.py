# Generated by Django 5.0.1 on 2024-02-27 13:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_owner', '0008_requiredwagons_capacity_requiredwagons_net_weight_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requiredwagons',
            options={'verbose_name': 'واگن مورد نیاز', 'verbose_name_plural': 'واگن های مورد نیاز'},
        ),
        migrations.RemoveField(
            model_name='requiredwagons',
            name='inner_cargo',
        ),
        migrations.RemoveField(
            model_name='requiredwagons',
            name='international_cargo',
        ),
        migrations.AddField(
            model_name='requiredwagons',
            name='counter',
            field=models.IntegerField(default=0, verbose_name='تعداد واگن'),
        ),
        migrations.AddField(
            model_name='requiredwagons',
            name='rail_cargo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rail_cargo_related_name', to='goods_owner.railcargo', verbose_name='اعلام بار ریلی'),
        ),
        migrations.AlterField(
            model_name='requiredwagons',
            name='net_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='وزن خالص محموله'),
        ),
    ]