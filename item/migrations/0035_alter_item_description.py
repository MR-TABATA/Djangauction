# Generated by Django 4.2.3 on 2023-11-03 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0034_alter_item_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='商品説明'),
        ),
    ]