# Generated by Django 4.2.3 on 2023-09-29 01:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0008_alter_stat_custom_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stat',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner_item', to='item.item'),
        ),
    ]
