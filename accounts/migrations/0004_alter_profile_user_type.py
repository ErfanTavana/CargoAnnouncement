# Generated by Django 5.0.1 on 2024-02-25 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_driver_cooperate_with_carrier_owners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[(0, 'انتخاب نشده'), (1, 'صاحب بار'), (2, 'صاحب حمل کننده'), (3, 'راننده'), (4, 'ادمین')], default='انتخاب نشده', max_length=255, verbose_name='نوع کاربر'),
        ),
    ]
