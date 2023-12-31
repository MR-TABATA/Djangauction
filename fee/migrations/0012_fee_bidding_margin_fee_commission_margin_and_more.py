# Generated by Django 4.2.3 on 2023-10-31 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0011_userfee'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='bidding_margin',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True, verbose_name='落札手数料マージン'),
        ),
        migrations.AddField(
            model_name='fee',
            name='commission_margin',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True, verbose_name='成約手数料マージン'),
        ),
        migrations.AddField(
            model_name='fee',
            name='display_margin',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True, verbose_name='出品手数料マージン'),
        ),
    ]
