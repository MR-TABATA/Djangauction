# Generated by Django 4.2.3 on 2023-09-28 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_alter_item_options_alter_item_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='商品説明'),
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='種類'),
        ),
    ]
