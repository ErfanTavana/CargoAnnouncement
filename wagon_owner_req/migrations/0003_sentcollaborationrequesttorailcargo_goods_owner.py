# Generated by Django 5.0.1 on 2024-02-28 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_profile_user_type_wagonowner'),
        ('wagon_owner_req', '0002_sentcollaborationrequesttorailcargo_cargo_wagon_coordination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentcollaborationrequesttorailcargo',
            name='goods_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.goodsowner', verbose_name='پروفایل صاحب بار'),
        ),
    ]
