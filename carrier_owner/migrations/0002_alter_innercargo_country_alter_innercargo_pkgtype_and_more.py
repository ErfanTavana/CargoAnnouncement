# Generated by Django 5.0.1 on 2024-01-21 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrier_owner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='innercargo',
            name='country',
            field=models.CharField(blank=True, choices=[('ایران', 'ایران'), ('روسیه', 'روسیه'), ('قزاقستان', 'قزاقستان'), ('ازبکستان', 'ازبکستان'), ('قرقیزستان', 'قرقیزستان'), ('تاجیکستان', 'تاجیکستان'), ('7افغانستان', 'افغانستان'), ('ارمنستان', 'ارمنستان')], max_length=20, null=True, verbose_name='کشور مبدا'),
        ),
        migrations.AlterField(
            model_name='innercargo',
            name='pkgType',
            field=models.CharField(blank=True, choices=[('کیسه', 'کیسه'), ('فله', 'فله'), ('پالت', 'پالت'), ('جامبو', 'جامبو'), ('کانتینر', 'کانتینر'), ('بندی', 'بندی'), ('رول', 'رول'), ('سواری', 'سواری'), ('جعبه', 'جعبه'), ('کالای خاص', 'کالای خاص'), ('غیر پالیتیزه', 'غیر پالیتیزه'), ('غیرمعمول', 'غیرمعمول')], max_length=20, null=True, verbose_name='نوع بسته بندی'),
        ),
        migrations.AlterField(
            model_name='innercargo',
            name='specialWidgets',
            field=models.CharField(blank=True, choices=[('روباری', 'روباری'), ('نیاز به بارنامه ندارد', 'نیاز به بارنامه ندارد'), ('بارنامه خودم میگیرم', 'بارنامه خودم میگیرم')], max_length=100, null=True, verbose_name='ویژگی های خاص'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='country',
            field=models.CharField(blank=True, choices=[('ایران', 'ایران'), ('روسیه', 'روسیه'), ('قزاقستان', 'قزاقستان'), ('ازبکستان', 'ازبکستان'), ('قرقیزستان', 'قرقیزستان'), ('تاجیکستان', 'تاجیکستان'), ('7افغانستان', 'افغانستان'), ('ارمنستان', 'ارمنستان')], max_length=20, null=True, verbose_name='کشور مبدا'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='pkgType',
            field=models.CharField(blank=True, choices=[('کیسه', 'کیسه'), ('فله', 'فله'), ('پالت', 'پالت'), ('جامبو', 'جامبو'), ('کانتینر', 'کانتینر'), ('بندی', 'بندی'), ('رول', 'رول'), ('سواری', 'سواری'), ('جعبه', 'جعبه'), ('کالای خاص', 'کالای خاص'), ('غیر پالیتیزه', 'غیر پالیتیزه'), ('غیرمعمول', 'غیرمعمول')], max_length=20, null=True, verbose_name='نوع بسته بندی'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='senderCountry',
            field=models.CharField(blank=True, choices=[('ایران', 'ایران'), ('روسیه', 'روسیه'), ('قزاقستان', 'قزاقستان'), ('ازبکستان', 'ازبکستان'), ('قرقیزستان', 'قرقیزستان'), ('تاجیکستان', 'تاجیکستان'), ('7افغانستان', 'افغانستان'), ('ارمنستان', 'ارمنستان')], max_length=20, null=True, verbose_name='کشور مبدا'),
        ),
        migrations.AlterField(
            model_name='internationalcargo',
            name='specialWidgets',
            field=models.CharField(blank=True, choices=[('روباری', 'روباری'), ('نیاز به بارنامه ندارد', 'نیاز به بارنامه ندارد'), ('بارنامه خودم میگیرم', 'بارنامه خودم میگیرم')], max_length=100, null=True, verbose_name='ویژگی های خاص'),
        ),
    ]
