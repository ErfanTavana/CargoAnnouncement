# Generated by Django 5.0.1 on 2024-03-06 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('E_Wallet', '0002_alter_wallettransaction_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallettransaction',
            name='amount',
            field=models.IntegerField(verbose_name='مقدار تراکنش'),
        ),
    ]