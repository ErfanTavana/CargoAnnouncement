# Generated by Django 5.0.1 on 2024-03-06 06:16

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
            name='WagonDetails',
            fields=[
                ('id', models.CharField(default=goods_owner.models.generate_complex_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('owner_type', models.CharField(blank=True, choices=[('خصوصی', 'خصوصی'), ('دولتی', 'دولتی')], default='', max_length=100, null=True, verbose_name='نوع مالکیت')),
                ('line_type', models.CharField(blank=True, choices=[('عریض', 'عریض'), ('نرمال', 'نرمال')], default='', max_length=8, null=True, verbose_name='نوع گیج/ خط')),
                ('wagon_type', models.CharField(blank=True, choices=[('مسقف', 'مسقف'), ('فله بر', 'فله بر'), ('مسطح', 'مسطح'), ('یخچال دار', 'یخچال دار'), ('مخزن دار', 'مخزن دار'), ('لبه بلند', 'لبه بلند'), ('لبه کوتاه', 'لبه کوتاه'), ('حمل خودرو', 'حمل خودرو')], max_length=20, null=True, verbose_name='نوع واگن')),
                ('capacity', models.CharField(blank=True, choices=[('واگن 24', 'واگن 24'), ('واگن 26', 'واگن 26'), ('واگن 28', 'واگن 28'), ('واگن 29', 'واگن 29'), ('سایر', 'سایر')], default='', max_length=20, null=True, verbose_name='ظرفیت حمل')),
                ('others', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='سایر')),
                ('wagon_docs', models.ImageField(blank=True, default='', max_length=800, null=True, storage=5000, upload_to='', verbose_name='آپلود مجوز واگن')),
                ('carrier_price', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, verbose_name='قیمت حمل و نقل')),
                ('wagon_counts', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='تعداد واگن')),
                ('wagon_nums', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='شماره واگن')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='حذف شده توسط ')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('wagon_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.wagonowner', verbose_name='صاحب واگن')),
            ],
            options={
                'verbose_name': 'جزئیات واگن',
                'verbose_name_plural': 'جزئیات واگن ها',
            },
        ),
    ]
