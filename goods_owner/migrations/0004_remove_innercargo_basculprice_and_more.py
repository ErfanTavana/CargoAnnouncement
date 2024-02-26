# Generated by Django 5.0.1 on 2024-02-25 11:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_owner', '0003_cargofleetcoordination'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='innercargo',
            name='basculPrice',
        ),
        migrations.RemoveField(
            model_name='innercargo',
            name='loadigPrice',
        ),
        migrations.RemoveField(
            model_name='innercargo',
            name='sendersFamName',
        ),
        migrations.RemoveField(
            model_name='innercargo',
            name='storageBillNum',
        ),
        migrations.RemoveField(
            model_name='innercargo',
            name='storagePrice',
        ),
        migrations.RemoveField(
            model_name='internationalcargo',
            name='basculPrice',
        ),
        migrations.RemoveField(
            model_name='internationalcargo',
            name='loadigPrice',
        ),
        migrations.RemoveField(
            model_name='internationalcargo',
            name='sendersFamName',
        ),
        migrations.RemoveField(
            model_name='internationalcargo',
            name='storageBillNum',
        ),
        migrations.RemoveField(
            model_name='internationalcargo',
            name='storagePrice',
        ),
        migrations.AddField(
            model_name='innercargo',
            name='approximate_weight_per_packaging',
            field=models.FloatField(blank=True, null=True, verbose_name='وزن حدودی هر یک بسته بندی'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='approximate_weight_per_type',
            field=models.FloatField(blank=True, null=True, verbose_name='وزن حدودی هر تیپ'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='is_all_cargo_type',
            field=models.BooleanField(default=False, verbose_name='آیا تمام بار تیپ است؟'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='need_warehouse',
            field=models.BooleanField(default=False, verbose_name='آیا نیاز به انبار دارید؟'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='pallet_arrangement_type',
            field=models.CharField(blank=True, choices=[('کف', 'کف'), ('طبقاتی', 'طبقاتی')], max_length=50, null=True, verbose_name='نوع چیدمان پالت'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='pallet_size',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='سایز پالت (مشخصات بسته بندی)'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='sender_additional_requests',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='درخواست های تکمیلی فرستنده'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='specialized_lashing_required',
            field=models.BooleanField(default=False, verbose_name='آیا بار نیاز به مهار بندی تخصصی دارد؟'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='specialized_lashing_type_description',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='توضیح نوع مهار بندی تخصصی'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='specialized_lashing_type_upload',
            field=models.ImageField(blank=True, null=True, upload_to='lashing_types/', verbose_name='آپلود نوع مهار بندی تخصصی'),
        ),
        migrations.AddField(
            model_name='innercargo',
            name='warehouse_duration',
            field=models.DurationField(blank=True, null=True, verbose_name='مدت زمان انبار داری'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='approximate_weight_per_packaging',
            field=models.FloatField(blank=True, null=True, verbose_name='وزن حدودی هر یک بسته بندی'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='approximate_weight_per_type',
            field=models.FloatField(blank=True, null=True, verbose_name='وزن حدودی هر تیپ'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='is_all_cargo_type',
            field=models.BooleanField(default=False, verbose_name='آیا تمام بار تیپ است؟'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='need_warehouse',
            field=models.BooleanField(default=False, verbose_name='آیا نیاز به انبار دارید؟'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='pallet_arrangement_type',
            field=models.CharField(blank=True, choices=[('کف', 'کف'), ('طبقاتی', 'طبقاتی')], max_length=50, null=True, verbose_name='نوع چیدمان پالت'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='pallet_size',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='سایز پالت (مشخصات بسته بندی)'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='sender_additional_requests',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='درخواست های تکمیلی فرستنده'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='specialized_lashing_required',
            field=models.BooleanField(default=False, verbose_name='آیا بار نیاز به مهار بندی تخصصی دارد؟'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='specialized_lashing_type_description',
            field=models.TextField(blank=True, max_length=5000, null=True, verbose_name='توضیح نوع مهار بندی تخصصی'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='specialized_lashing_type_upload',
            field=models.ImageField(blank=True, null=True, upload_to='lashing_types/', verbose_name='آپلود نوع مهار بندی تخصصی'),
        ),
        migrations.AddField(
            model_name='internationalcargo',
            name='warehouse_duration',
            field=models.DurationField(blank=True, null=True, verbose_name='مدت زمان انبار داری'),
        ),
        migrations.AlterField(
            model_name='innercargo',
            name='destination_area',
            field=models.CharField(blank=True, choices=[('گمرگ', 'گمرگ'), ('بندر', 'بندر'), ('ایستگاه', 'ایستگاه'), ('گمرک/ایستگاه', 'گمرک/ایستگاه')], max_length=100, null=True, verbose_name='محدوده مقصد'),
        ),
        migrations.AlterField(
            model_name='innercargo',
            name='destination_custom_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام  مقصد'),
        ),
        migrations.AlterField(
            model_name='innercargo',
            name='duratio_ndischargeTime',
            field=models.DurationField(blank=True, default=datetime.timedelta(0), max_length=200, null=True, verbose_name=' مدت زمان تخلیه بار در مقصد'),
        ),
        migrations.AlterField(
            model_name='innercargo',
            name='sendersName',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام و نام خانوادگی فرستنده'),
        ),
        migrations.AlterField(
            model_name='innercargo',
            name='specialWidgets',
            field=models.CharField(blank=True, choices=[('روباری', 'روباری'), ('نیاز به بارنامه ندارد', 'نیاز به بارنامه ندارد'), ('بارنامه خودم میگیرم', 'بارنامه خودم میگیرم'), ('درخواست بارنامه', 'درخواست بارنامه')], max_length=100, null=True, verbose_name='ویژگی های خاص'),
        ),
        migrations.AlterField(
            model_name='innercargo',
            name='weekly_days',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='روزهای هفته'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='destination_area',
            field=models.CharField(blank=True, choices=[('گمرگ', 'گمرگ'), ('بندر', 'بندر'), ('ایستگاه', 'ایستگاه'), ('گمرک/ایستگاه', 'گمرک/ایستگاه')], max_length=100, null=True, verbose_name='محدوده مقصد'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='destination_custom_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام  مقصد'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='duratio_ndischargeTime',
            field=models.DurationField(blank=True, default=datetime.timedelta(0), max_length=200, null=True, verbose_name=' مدت زمان تخلیه بار در مقصد'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='sendersName',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام و نام خانوادگی فرستنده'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='specialWidgets',
            field=models.CharField(blank=True, choices=[('روباری', 'روباری'), ('نیاز به بارنامه ندارد', 'نیاز به بارنامه ندارد'), ('بارنامه خودم میگیرم', 'بارنامه خودم میگیرم'), ('درخواست بارنامه', 'درخواست بارنامه')], max_length=100, null=True, verbose_name='ویژگی های خاص'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='weekly_days',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='روزهای هفته'),
        ),
    ]