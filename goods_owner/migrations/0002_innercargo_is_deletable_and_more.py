# Generated by Django 5.0.1 on 2024-01-28 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_owner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='innercargo',
            name='is_deletable',
            field=models.BooleanField(default=True, verbose_name='قابل حذف است ؟'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='is_deletable',
            field=models.BooleanField(default=True, verbose_name='قابل حذف است ؟'),
        ),
        migrations.AddField(
            model_name='requiredcarrier',
            name='is_deletable',
            field=models.BooleanField(default=True, verbose_name='قابل حذف است ؟'),
        ),
    ]
