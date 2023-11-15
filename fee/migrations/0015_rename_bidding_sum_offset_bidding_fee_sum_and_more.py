# Generated by Django 4.2.3 on 2023-11-02 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fee', '0014_offset_counterbalance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offset',
            old_name='bidding_sum',
            new_name='bidding_fee_sum',
        ),
        migrations.RenameField(
            model_name='offset',
            old_name='commission_sum',
            new_name='commission_fee_sum',
        ),
        migrations.RenameField(
            model_name='offset',
            old_name='display_sum',
            new_name='display_fee_sum',
        ),
        migrations.RemoveField(
            model_name='fee',
            name='display_margin',
        ),
        migrations.AddField(
            model_name='fee',
            name='systemUsageByYear',
            field=models.IntegerField(blank=True, null=True, verbose_name='システム年利用料'),
        ),
        migrations.AddField(
            model_name='offset',
            name='bidded_sum',
            field=models.IntegerField(blank=True, null=True, verbose_name='落札合計金額'),
        ),
        migrations.AddField(
            model_name='offset',
            name='commissioned_sum',
            field=models.IntegerField(blank=True, null=True, verbose_name='成約合計金額'),
        ),
        migrations.AddField(
            model_name='offset',
            name='fee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offset_fee', to='fee.fee'),
        ),
    ]
