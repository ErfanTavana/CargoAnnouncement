# Generated by Django 5.0.1 on 2024-02-02 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_owner', '0004_remove_goodsownerreqcarow_required_carrier'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsownerreqcarow',
            name='inner_cargo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inner_cargo_carriers2', to='goods_owner.innercargo', verbose_name='اعلام بار داخلی'),
        ),
        migrations.AddField(
            model_name='goodsownerreqcarow',
            name='international_cargo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='international_cargo_carriers2', to='goods_owner.internationalcargo', verbose_name='اعلام بار خارجی'),
        ),
    ]
