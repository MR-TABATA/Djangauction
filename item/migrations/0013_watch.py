# Generated by Django 4.2.3 on 2023-10-06 01:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0012_alter_stat_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='生成日時')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='削除日時')),
                ('custom_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='watch_user', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='watch_item', to='item.item')),
            ],
            options={
                'verbose_name': 'お気に入り',
                'verbose_name_plural': 'お気に入り',
                'db_table': 'da_watch',
            },
        ),
    ]