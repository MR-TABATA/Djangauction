# Generated by Django 4.2.3 on 2023-09-26 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0003_rename_setion_fee_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='top_display',
            field=models.CharField(blank=True, default='show', max_length=20, null=True, verbose_name='トップ画面表示対象'),
        ),
    ]
