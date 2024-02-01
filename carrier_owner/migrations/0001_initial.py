# Generated by Django 5.0.1 on 2024-02-01 04:25

import django.db.models.deletion
import django.utils.timezone
import goods_owner.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('goods_owner', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadFleet',
            fields=[
                ('id', models.CharField(default=goods_owner.models.generate_complex_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('ownerType', models.CharField(choices=[('مالکیتی', 'مالکیتی'), ('شرکتی', 'شرکتی')], default='', max_length=100, verbose_name='نوع مالکیت')),
                ('roomType', models.CharField(choices=[('چادری', 'چادری'), ('روباز', 'روباز'), ('یخچالی', 'یخچالی')], default='', max_length=100, verbose_name='نوع اتاق')),
                ('vehichleType', models.CharField(choices=[('ماشین باربری کوچک و سبک', 'ماشین باربری کوچک و سبک'), ('ماشین باربری نیمه سنگین', 'ماشین باربری نیمه سنگین'), ('ماشین حمل بار سنگین', 'ماشین حمل بار سنگین')], default='', max_length=100, verbose_name='نوع وسیله حمل کننده')),
                ('semiHeavyVehichle', models.CharField(choices=[('کامیون', 'کامیون'), ('خاور', 'خاور'), ('هیوندا', 'هیوندا'), ('ماشین باربری ایسوزو', 'ماشین باربری ایسوزو'), ('کامیونت', 'کامیونت')], default='', max_length=20, verbose_name='ماشین باربری نیمه سنگین')),
                ('semiHeavyVehichleOthers', models.CharField(default='', max_length=100, verbose_name='سایر')),
                ('HeavyVehichle', models.CharField(choices=[('تریلی', 'تریلی'), ('ترانزیت', 'ترانزیت'), ('ده تن', 'ده تن'), ('کفی', 'کفی'), ('ترانزیت یخچالی', 'ترانزیت یخچالی'), ('بیست تن', 'بیست تن'), ('چادری سه محور', 'چادری سه محور'), ('کمپرسی', 'کمپرسی'), ('تریلی تانکر فاو', 'تریلی تانکر فاو')], default='', max_length=20, verbose_name='ماشین باربری سنگین')),
                ('heavy_vehicle_others', models.CharField(default='', max_length=100, verbose_name='سایر')),
                ('plaque_one_num_check', models.BooleanField(default='', verbose_name='شماره پلاک واحد(تک پلاک)')),
                ('plaque_one_num', models.CharField(default='', max_length=9, verbose_name='ثبت شماره پلاک واحد(تک پلاک)')),
                ('plaque_puller_num_check', models.BooleanField(default='', verbose_name='شماره پلاک کشنده')),
                ('plaque_puller_num', models.CharField(default='', max_length=9, verbose_name='ثبت شماره پلاک کشنده')),
                ('plaque_carriage_num_check', models.BooleanField(default='', verbose_name='شماره پلاک گاری')),
                ('plaque_carriage_num', models.CharField(default='', max_length=9, verbose_name='ثبت شماره پلاک گاری')),
                ('plaque_container_num_check', models.BooleanField(default='', verbose_name='شماره پلاک کانتینر')),
                ('plaque_container_num', models.CharField(default='', max_length=9, verbose_name='ثبت شماره پلاک کانتینر')),
                ('vehicle_card', models.ImageField(blank=True, default='', max_length=800, null=True, upload_to='', verbose_name='آپلود کارت ماشین')),
                ('vehicle_card_bool', models.BooleanField(default=False, verbose_name='آپلود کارت ماشین')),
                ('vehicle_property_doc', models.ImageField(blank=True, default='', max_length=800, null=True, upload_to='', verbose_name='آپلود برگه سبز ماشین')),
                ('vehicle_property_doc_bool', models.BooleanField(default=False, verbose_name='آپلود برگه سبز ماشین')),
                ('vehicle_advocate_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ اعتبار بیمه نامه ماشین')),
                ('vehicle_advocate', models.ImageField(blank=True, default='', max_length=800, null=True, upload_to='', verbose_name='آپلود بیمه نامه ماشین')),
                ('vehicle_advocate_bool', models.BooleanField(default=False, verbose_name='آپلود بیمه نامه ماشین')),
                ('code_id', models.CharField(default='', max_length=12, verbose_name='کد ملی  / شماره پاسپورت مالک')),
                ('owner_document', models.ImageField(blank=True, default='', max_length=800, null=True, upload_to='', verbose_name='آپلود کارت ملی / پاسپورت مالک')),
                ('international_docs', models.ImageField(blank=True, default='', max_length=800, null=True, upload_to='', verbose_name='آپلود مدارک مجوز حمل بین المللی در صورت وجود')),
                ('international_docs_bool', models.BooleanField(default=False, verbose_name='آپلود مدارک مجوز حمل بین المللی در صورت وجود')),
                ('carrier_type', models.CharField(choices=[('حمل و نقل داخلی', 'حمل و نقل داخلی'), ('حمل و نقل بین المللی', 'حمل و نقل بین المللی')], default='حمل و نقل بین المللی', max_length=30, verbose_name='نوع حمل و نقل')),
                ('carrier_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.carrierowner', verbose_name='صاحب حمل کننده')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='required_carriers', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'حمل کننده های مربوط به صاحب حمل کننده',
                'verbose_name_plural': 'حمل کننده های مربوط به صاحاب حمل کنندهها ',
            },
        ),
        migrations.CreateModel(
            name='CarOwReqGoodsOwner',
            fields=[
                ('id', models.CharField(default=goods_owner.models.generate_complex_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('proposed_price', models.FloatField(default=0.0, verbose_name='قیمت پیشنهادی')),
                ('request_result', models.CharField(choices=[('در انتظار پاسخ', 'در انتظار پاسخ'), ('تایید شده', 'تایید شده'), ('رد شده', 'رد شده'), ('لغو شده', 'لغو شده')], max_length=30, verbose_name='نتیجه درخواست')),
                ('cancellation_time', models.DateTimeField(blank=True, null=True, verbose_name='زمان لغو درخواست')),
                ('carrier_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.carrierowner', verbose_name='صاحب حمل کننده')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL)),
                ('goods_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.goodsowner', verbose_name='صاحب بار')),
                ('required_carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods_owner.requiredcarrier', verbose_name='درخواست صاحب بار')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('road_fleet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_owners', to='carrier_owner.roadfleet', verbose_name='حمل کننده')),
            ],
            options={
                'verbose_name': 'درخواست همکاری صاحب حمل کننده از صاحب بار',
                'verbose_name_plural': 'درخواست\u200cهای همکاری صاحب حمل کننده از صاحب بار',
            },
        ),
        migrations.CreateModel(
            name='CarOwReqDriver',
            fields=[
                ('id', models.CharField(default=goods_owner.models.generate_complex_id, editable=False, max_length=10, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('collaboration_type', models.CharField(choices=[('همکاری دائم (تمام وقت)', 'همکاری دائم (تمام وقت)'), ('همکاری موقت (پاره وقت)', 'همکاری موقت (پاره وقت)')], max_length=40, verbose_name='نوع همکاری')),
                ('origin', models.CharField(max_length=255, verbose_name='مبدا')),
                ('destination', models.CharField(max_length=255, verbose_name='مقصد')),
                ('proposed_price', models.FloatField(default=0.0, verbose_name='قیمت پیشنهادی')),
                ('request_result', models.CharField(choices=[('در انتظار پاسخ', 'در انتظار پاسخ'), ('تایید شده', 'تایید شده'), ('رد شده', 'رد شده'), ('لغو شده', 'لغو شده')], max_length=30, verbose_name='نتیجه درخواست')),
                ('cancellation_time', models.DateTimeField(blank=True, null=True, verbose_name='زمان لغو درخواست')),
                ('carrier_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.carrierowner', verbose_name='صاحب حمل کننده')),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.driver', verbose_name='راننده')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carrier_owner.roadfleet', verbose_name='حمل کننده')),
            ],
            options={
                'verbose_name': 'درخواست همکاری صاحب حمل کننده از راننده',
                'verbose_name_plural': 'درخواست\u200cهای همکاری صاحب حمل کننده از راننده',
            },
        ),
    ]
