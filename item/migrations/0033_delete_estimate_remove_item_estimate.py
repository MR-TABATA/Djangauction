# Generated by Django 4.2.3 on 2023-11-03 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0032_alter_item_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Estimate',
        ),
        migrations.RemoveField(
            model_name='item',
            name='estimate',
        ),
    ]
