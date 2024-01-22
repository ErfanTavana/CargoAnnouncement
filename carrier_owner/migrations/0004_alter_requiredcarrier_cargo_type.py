# Generated by Django 5.0.1 on 2024-01-21 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrier_owner', '0003_alter_innercargo_user_alter_internationalcargo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requiredcarrier',
            name='cargo_type',
            field=models.CharField(choices=[('اعلام بار داخلی', 'اعلام بار داخلی'), ('اعلام بار خارجی', 'اعلام بار خارجی'), ('اعلام بار ریلی', 'اعلام بار ریلی')], max_length=20, verbose_name='نوع بار'),
        ),
    ]