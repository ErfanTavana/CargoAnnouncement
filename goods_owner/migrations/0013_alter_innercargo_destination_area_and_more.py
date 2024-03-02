# Generated by Django 5.0.1 on 2024-03-02 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_owner', '0012_delete_goodsownerreqcarow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='innercargo',
            name='destination_area',
            field=models.CharField(blank=True, choices=[('گمرک', 'گمرک'), ('بندر', 'بندر'), ('ایستگاه', 'ایستگاه'), ('گمرک/ایستگاه', 'گمرک/ایستگاه')], max_length=100, null=True, verbose_name='محدوده مقصد'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='destination_area',
            field=models.CharField(blank=True, choices=[('گمرک', 'گمرک'), ('بندر', 'بندر'), ('ایستگاه', 'ایستگاه'), ('گمرک/ایستگاه', 'گمرک/ایستگاه')], max_length=100, null=True, verbose_name='محدوده مقصد'),
        ),
    ]
