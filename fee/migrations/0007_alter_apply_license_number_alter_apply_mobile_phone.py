# Generated by Django 4.2.3 on 2023-09-26 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0006_apply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='license_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='古物許可証番号'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='モバイル'),
        ),
    ]
