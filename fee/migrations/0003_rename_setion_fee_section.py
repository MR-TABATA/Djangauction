# Generated by Django 4.2.3 on 2023-09-25 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0002_alter_fee_bidding_alter_fee_commission_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fee',
            old_name='setion',
            new_name='section',
        ),
    ]
