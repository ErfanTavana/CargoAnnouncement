# Generated by Django 5.0.1 on 2024-01-30 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_owner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='innercargo',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
        migrations.AlterField(
            model_name='requiredcarrier',
            name='is_ok',
            field=models.BooleanField(default=True, verbose_name='آیا تایید شده است؟'),
        ),
    ]