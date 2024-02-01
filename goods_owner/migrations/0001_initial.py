# Generated by Django 5.0.1 on 2024-02-01 04:25

import datetime
import django.db.models.deletion
import django.utils.timezone
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
            name='InnerCargo',
            fields=[
                ('id', models.CharField(default=goods_owner.models.generate_complex_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('length', models.IntegerField(blank=True, default=0, null=True, verbose_name='طول')),
                ('width', models.IntegerField(blank=True, default=0, null=True, verbose_name='عرض')),
                ('height', models.IntegerField(blank=True, default=0, null=True, verbose_name='ارتفاع')),
                ('cargoType', models.CharField(blank=True, default='', max_length=800, null=True, verbose_name='عنوان محموله')),
                ('pkgType', models.CharField(blank=True, choices=[('کیسه', 'کیسه'), ('فله', 'فله'), ('پالت', 'پالت'), ('جامبو', 'جامبو'), ('کانتینر', 'کانتینر'), ('بندی', 'بندی'), ('رول', 'رول'), ('سواری', 'سواری'), ('جعبه', 'جعبه'), ('کالای خاص', 'کالای خاص'), ('غیر پالیتیزه', 'غیر پالیتیزه'), ('غیرمعمول', 'غیرمعمول')], max_length=20, null=True, verbose_name='نوع بسته بندی')),
                ('description', models.TextField(blank=True, default='', max_length=5000, null=True, verbose_name='توضیحات')),
                ('specialWidgets', models.CharField(blank=True, choices=[('روباری', 'روباری'), ('نیاز به بارنامه ندارد', 'نیاز به بارنامه ندارد'), ('بارنامه خودم میگیرم', 'بارنامه خودم میگیرم')], max_length=100, null=True, verbose_name='ویژگی های خاص')),
                ('storageBillNum', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='شماره قبض انبار')),
                ('storagePrice', models.TextField(blank=True, default='', max_length=9999, null=True, verbose_name='هزینه انبارداری')),
                ('loadigPrice', models.TextField(blank=True, default='', max_length=9999, null=True, verbose_name='هزینه بارگیری')),
                ('basculPrice', models.TextField(blank=True, default='', max_length=9999, null=True, verbose_name='هزینه باسکول')),
                ('specialDesc', models.TextField(blank=True, default='', max_length=9999, null=True, verbose_name='توضیحات خاص')),
                ('sendersName', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام فرستنده')),
                ('sendersFamName', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام خانوادگی فرستنده')),
                ('senderMobileNum', models.CharField(blank=True, default='', max_length=12, null=True, verbose_name='شماره تلفن / موبایل فرستنده')),
                ('dischargeTimeDate', models.DateTimeField(blank=True, default=django.utils.timezone.now, max_length=200, null=True, verbose_name='تاریخ و ساعت تحویل بار در مقصد')),
                ('duratio_ndischargeTime', models.DurationField(blank=True, default=datetime.timedelta(0), max_length=200, null=True, verbose_name='مدت زمان تخلیه بار در مقصد')),
                ('country', models.CharField(blank=True, choices=[('ایران', 'ایران'), ('روسیه', 'روسیه'), ('قزاقستان', 'قزاقستان'), ('ازبکستان', 'ازبکستان'), ('قرقیزستان', 'قرقیزستان'), ('تاجیکستان', 'تاجیکستان'), ('7افغانستان', 'افغانستان'), ('ارمنستان', 'ارمنستان')], max_length=20, null=True, verbose_name='کشور مبدا')),
                ('delivery_provider_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام شرکت تحویل دهنده')),
                ('delivery_provider_national_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='شناسه ملی تحویل دهنده')),
                ('delivery_provider_full_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='نام و نام خانوادگی تحویل دهنده')),
                ('delivery_provider_mobile', models.CharField(blank=True, max_length=12, null=True, verbose_name='شماره موبایل مدیر عامل تحویل دهنده')),
                ('cargo_receiver_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام شرکت تحویل گیرنده')),
                ('cargo_receiver_national_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='شناسه ملی تحویل گیرنده')),
                ('cargo_receiver_full_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='نام و نام خانوادگی تحویل گیرنده')),
                ('cargo_receiver_mobile', models.CharField(blank=True, max_length=12, null=True, verbose_name='شماره موبایل مدیر عامل تحویل گیرنده')),
                ('state', models.CharField(blank=True, max_length=20, null=True, verbose_name='استان مبدا')),
                ('city', models.CharField(blank=True, max_length=20, null=True, verbose_name='شهر / منطقه / محدوده مبدا')),
                ('street', models.CharField(blank=True, max_length=50, null=True, verbose_name='خیابان مبدا')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='آدرس دقیق مبدا')),
                ('customName', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام کمرگ مبدا')),
                ('deliveryTimeDate', models.DateTimeField(blank=True, default=django.utils.timezone.now, max_length=200, null=True, verbose_name='تاریخ و ساعت تحویل بار در مبدا')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL)),
                ('goods_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.goodsowner', verbose_name='پروفایل صاحب بار')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'اعلام بار داخلی',
                'verbose_name_plural': 'اعلام بار های  داخلی',
            },
        ),
        migrations.CreateModel(
            name='InternationalCargo',
            fields=[
                ('id', models.CharField(default=goods_owner.models.generate_complex_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('length', models.IntegerField(blank=True, default=0, null=True, verbose_name='طول')),
                ('width', models.IntegerField(blank=True, default=0, null=True, verbose_name='عرض')),
                ('height', models.IntegerField(blank=True, default=0, null=True, verbose_name='ارتفاع')),
                ('cargoType', models.CharField(blank=True, default='', max_length=800, null=True, verbose_name='عنوان محموله')),
                ('pkgType', models.CharField(blank=True, choices=[('کیسه', 'کیسه'), ('فله', 'فله'), ('پالت', 'پالت'), ('جامبو', 'جامبو'), ('کانتینر', 'کانتینر'), ('بندی', 'بندی'), ('رول', 'رول'), ('سواری', 'سواری'), ('جعبه', 'جعبه'), ('کالای خاص', 'کالای خاص'), ('غیر پالیتیزه', 'غیر پالیتیزه'), ('غیرمعمول', 'غیرمعمول')], max_length=20, null=True, verbose_name='نوع بسته بندی')),
                ('description', models.TextField(blank=True, default='', max_length=5000, null=True, verbose_name='توضیحات')),
                ('specialWidgets', models.CharField(blank=True, choices=[('روباری', 'روباری'), ('نیاز به بارنامه ندارد', 'نیاز به بارنامه ندارد'), ('بارنامه خودم میگیرم', 'بارنامه خودم میگیرم')], max_length=100, null=True, verbose_name='ویژگی های خاص')),
                ('storageBillNum', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='شماره قبض انبار')),
                ('storagePrice', models.TextField(blank=True, default='', max_length=9999, null=True, verbose_name='هزینه انبارداری')),
                ('loadigPrice', models.TextField(blank=True, default='', max_length=9999, null=True, verbose_name='هزینه بارگیری')),
                ('basculPrice', models.TextField(blank=True, default='', max_length=9999, null=True, verbose_name='هزینه باسکول')),
                ('specialDesc', models.TextField(blank=True, default='', max_length=9999, null=True, verbose_name='توضیحات خاص')),
                ('sendersName', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام فرستنده')),
                ('sendersFamName', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام خانوادگی فرستنده')),
                ('senderMobileNum', models.CharField(blank=True, default='', max_length=12, null=True, verbose_name='شماره تلفن / موبایل فرستنده')),
                ('duratio_ndischargeTime', models.DurationField(blank=True, default=datetime.timedelta(0), max_length=200, null=True, verbose_name='مدت زمان تخلیه بار در مقصد')),
                ('country', models.CharField(blank=True, choices=[('ایران', 'ایران'), ('روسیه', 'روسیه'), ('قزاقستان', 'قزاقستان'), ('ازبکستان', 'ازبکستان'), ('قرقیزستان', 'قرقیزستان'), ('تاجیکستان', 'تاجیکستان'), ('7افغانستان', 'افغانستان'), ('ارمنستان', 'ارمنستان')], max_length=20, null=True, verbose_name='کشور مبدا')),
                ('delivery_provider_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام شرکت تحویل دهنده')),
                ('delivery_provider_national_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='شناسه ملی تحویل دهنده')),
                ('delivery_provider_full_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='نام و نام خانوادگی تحویل دهنده')),
                ('delivery_provider_mobile', models.CharField(blank=True, max_length=12, null=True, verbose_name='شماره موبایل مدیر عامل تحویل دهنده')),
                ('cargo_receiver_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام شرکت تحویل گیرنده')),
                ('cargo_receiver_national_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='شناسه ملی تحویل گیرنده')),
                ('cargo_receiver_full_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='نام و نام خانوادگی تحویل گیرنده')),
                ('cargo_receiver_mobile', models.CharField(blank=True, max_length=12, null=True, verbose_name='شماره موبایل مدیر عامل تحویل گیرنده')),
                ('state', models.CharField(blank=True, max_length=20, null=True, verbose_name='استان مبدا')),
                ('city', models.CharField(blank=True, max_length=20, null=True, verbose_name='شهر / منطقه / محدوده مبدا')),
                ('street', models.CharField(blank=True, max_length=50, null=True, verbose_name='خیابان مبدا')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='آدرس دقیق مبدا')),
                ('customName', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام کمرگ مبدا')),
                ('senderCountry', models.CharField(blank=True, choices=[('ایران', 'ایران'), ('روسیه', 'روسیه'), ('قزاقستان', 'قزاقستان'), ('ازبکستان', 'ازبکستان'), ('قرقیزستان', 'قرقیزستان'), ('تاجیکستان', 'تاجیکستان'), ('7افغانستان', 'افغانستان'), ('ارمنستان', 'ارمنستان')], max_length=255, null=True, verbose_name='کشور مبدا')),
                ('senderState', models.CharField(blank=True, max_length=20, null=True, verbose_name='استان مبدا')),
                ('senderCity', models.CharField(blank=True, max_length=20, null=True, verbose_name='شهر / منطقه / محدوده مبدا')),
                ('senderStreet', models.CharField(blank=True, max_length=50, null=True, verbose_name='خیابان')),
                ('senderAddress', models.CharField(blank=True, max_length=100, null=True, verbose_name='آدرس دقیق مبدا')),
                ('deliveryTimeDate', models.DateTimeField(blank=True, default=django.utils.timezone.now, max_length=200, null=True, verbose_name='تاریخ و ساعت تحویل بار در مبدا')),
                ('dischargeTimeDate', models.DateTimeField(blank=True, default=django.utils.timezone.now, max_length=200, null=True, verbose_name='تاریخ و ساعت تحویل بار در مقصد')),
                ('dischargeTime', models.DurationField(blank=True, default=datetime.timedelta(0), max_length=200, null=True, verbose_name='مدت زمان تخلیه بار در مقصد')),
                ('customNameEnd', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='نام کمرگ مقصد')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL)),
                ('goods_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.goodsowner', verbose_name='پروفایل صاحب بار')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'اعلام بار خارجی',
                'verbose_name_plural': 'اعلام بار های خارجی',
            },
        ),
        migrations.CreateModel(
            name='RequiredCarrier',
            fields=[
                ('id', models.CharField(default=goods_owner.models.generate_complex_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('relinquished', models.BooleanField(default=False, verbose_name='واگذار شده؟')),
                ('cargo_type', models.CharField(choices=[('اعلام بار داخلی', 'اعلام بار داخلی'), ('اعلام بار خارجی', 'اعلام بار خارجی'), ('اعلام بار ریلی', 'اعلام بار ریلی')], max_length=20, verbose_name='نوع بار')),
                ('cargo_weight', models.FloatField(max_length=100, verbose_name='وزن خالص محموله')),
                ('counter', models.PositiveIntegerField(verbose_name='تعداد حمل کننده مورد نیاز')),
                ('room_type', models.CharField(choices=[('چادری', 'چادری'), ('روباز', 'روباز'), ('یخچالی', 'یخچالی')], max_length=100, verbose_name='نوع اتاق مناسب')),
                ('vehichle_type', models.CharField(choices=[('ماشین باربری کوچک و سبک', 'ماشین باربری کوچک و سبک'), ('ماشین باربری نیمه سنگین', 'ماشین باربری نیمه سنگین'), ('ماشین حمل بار سنگین', 'ماشین حمل بار سنگین')], max_length=100, verbose_name='نوع وسیله حمل کننده مورد نیاز')),
                ('semi_heavy_vehichle', models.CharField(choices=[('کامیون', 'کامیون'), ('خاور', 'خاور'), ('هیوندا', 'هیوندا'), ('ماشین باربری ایسوزو', 'ماشین باربری ایسوزو'), ('کامیونت', 'کامیونت')], max_length=20, verbose_name='ماشین باربری نیمه سنگین ')),
                ('semi_heavy_vehichle_others', models.CharField(default='', max_length=100, verbose_name='سایر')),
                ('heavy_vehichle', models.CharField(choices=[('تریلی', 'تریلی'), ('ترانزیت', 'ترانزیت'), ('ده تن', 'ده تن'), ('کفی', 'کفی'), ('ترانزیت یخچالی', 'ترانزیت یخچالی'), ('بیست تن', 'بیست تن'), ('چادری سه محور', 'چادری سه محور'), ('کمپرسی', 'کمپرسی'), ('تریلی تانکر فاو', 'تریلی تانکر فاو')], max_length=20, verbose_name='ماشین باربری سنگین')),
                ('heavy_vehichle_others', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='سایر')),
                ('special_widget_carrier', models.TextField(blank=True, max_length=9999, null=True, verbose_name='ویژگی های خاص حمل کننده مورد نیاز')),
                ('carrier_price', models.IntegerField(blank=True, default=0, null=True, verbose_name='قیمت تقریبی حمل')),
                ('cargo_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='ارزش بار هر حمل کننده / خودرو')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL)),
                ('inner_cargo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inner_cargo_carriers', to='goods_owner.innercargo', verbose_name='اعلام بار داخلی')),
                ('international_cargo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='international_cargo_carriers', to='goods_owner.internationalcargo', verbose_name='اعلام بار خارجی')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'حمل\u200cکننده مورد نیاز اعلام بار',
                'verbose_name_plural': 'حمل\u200cکننده\u200cهای مورد نیاز اعلام بار',
            },
        ),
    ]
