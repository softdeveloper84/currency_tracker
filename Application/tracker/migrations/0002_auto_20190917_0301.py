# Generated by Django 3.0a1 on 2019-09-17 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencymodel',
            name='base',
            field=models.CharField(choices=[('USD', 'RUR')], max_length=10),
        ),
        migrations.AlterField(
            model_name='currencymodel',
            name='target',
            field=models.CharField(choices=[('USD', 'BTC')], max_length=10),
        ),
    ]
