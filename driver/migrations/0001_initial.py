# Generated by Django 5.0.1 on 2024-02-03 08:07

import django.db.models.deletion
import goods_owner.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverReqCarrierOwner',
            fields=[
                ('id', models.CharField(default=goods_owner.models.generate_complex_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('cargo_type', models.CharField(choices=[('اعلام بار داخلی', 'اعلام بار داخلی'), ('اعلام بار خارجی', 'اعلام بار خارجی'), ('اعلام بار ریلی', 'اعلام بار ریلی')], default='اعلام بار داخلی', max_length=20, verbose_name='نوع همکاری')),
                ('proposed_price', models.FloatField(default=0.0, verbose_name='قیمت پیشنهادی')),
                ('request_result', models.CharField(choices=[('در انتظار پاسخ', 'در انتظار پاسخ'), ('تایید شده', 'تایید شده'), ('رد شده', 'رد شده'), ('لغو شده', 'لغو شده')], max_length=30, verbose_name='نتیجه درخواست')),
                ('cancellation_time', models.DateTimeField(blank=True, null=True, verbose_name='زمان لغو درخواست')),
                ('source', models.CharField(blank=True, max_length=255, null=True, verbose_name='مبدا')),
                ('destination', models.CharField(blank=True, max_length=255, null=True, verbose_name='مقصد')),
                ('carrier_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.carrierowner', verbose_name='صاحب حمل کننده')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='required_carriers', to='accounts.driver', verbose_name='راننده')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'درخواست همکاری راننده از صاحب حمل کننده',
                'verbose_name_plural': 'درخواست های  همکاری راننده از صاحب حمل کننده',
            },
        ),
    ]
