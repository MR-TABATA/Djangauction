# Generated by Django 4.2.3 on 2023-11-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0033_delete_estimate_remove_item_estimate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='種類'),
        ),
    ]
