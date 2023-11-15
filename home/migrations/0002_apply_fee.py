# Generated by Django 4.2.3 on 2023-09-26 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0008_delete_apply'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apply_fee', to='fee.fee'),
        ),
    ]
