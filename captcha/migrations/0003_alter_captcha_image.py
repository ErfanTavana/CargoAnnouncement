# Generated by Django 5.0.1 on 2024-03-08 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('captcha', '0002_captcha_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captcha',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='captcha/'),
        ),
    ]