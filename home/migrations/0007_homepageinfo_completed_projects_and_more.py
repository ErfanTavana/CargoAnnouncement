# Generated by Django 5.0.1 on 2024-03-08 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_homepageinfo_international_truck_payment_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepageinfo',
            name='completed_projects',
            field=models.IntegerField(default=0, verbose_name='تعداد پروژه\u200cهای تکمیل شده'),
        ),
        migrations.AddField(
            model_name='homepageinfo',
            name='num_participants',
            field=models.IntegerField(default=0, verbose_name='تعداد شرکت\u200cکنندگان'),
        ),
        migrations.AddField(
            model_name='homepageinfo',
            name='num_sessions',
            field=models.IntegerField(default=0, verbose_name='تعداد جلسات آموزش'),
        ),
        migrations.AddField(
            model_name='homepageinfo',
            name='qrcode_image',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/', verbose_name='عکس کیو آر کد'),
        ),
        migrations.AddField(
            model_name='homepageinfo',
            name='training_hours',
            field=models.IntegerField(default=0, verbose_name='تعداد ساعات آموزش'),
        ),
    ]