# Generated by Django 5.0.1 on 2024-03-06 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_homepageinfo_carrier_owner_payment_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepageinfo',
            name='exporters_union_payment_rate',
            field=models.FloatField(blank=True, null=True, verbose_name='نرخ پرداختی اتحادیه صادرکنندگان'),
        ),
    ]
