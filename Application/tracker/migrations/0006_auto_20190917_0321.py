# Generated by Django 3.0a1 on 2019-09-17 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20190917_0308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencymodel',
            name='base',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='currencymodel',
            name='target',
            field=models.CharField(max_length=10),
        ),
    ]
