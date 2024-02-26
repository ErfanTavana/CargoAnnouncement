# Generated by Django 5.0.1 on 2024-02-26 06:19

import captcha.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Captcha',
            fields=[
                ('is_valid', models.BooleanField(auto_created=True, default=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='تاریخ حذف')),
                ('is_ok', models.BooleanField(default=True, verbose_name='آیا تایید شده است؟')),
                ('is_changeable', models.BooleanField(default=True, verbose_name='قابل تغییر است؟')),
                ('is_deletable', models.BooleanField(default=True, verbose_name='قابل حذف است؟')),
                ('id', models.CharField(default=captcha.models.generate_complex_id, max_length=18, primary_key=True, serialize=False, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('text', models.CharField(blank=True, max_length=200, null=True)),
                ('guide', models.CharField(blank=True, max_length=200, null=True)),
                ('answer', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deleted_by_%(class)s_set', to=settings.AUTH_USER_MODEL, verbose_name='حذف شده توسط ')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]