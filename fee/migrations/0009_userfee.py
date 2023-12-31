# Generated by Django 4.2.3 on 2023-10-15 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fee', '0008_delete_apply'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='生成日時')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='削除日時')),
                ('custom_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('fee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fee', to='fee.fee')),
            ],
            options={
                'verbose_name': '年会費・手数料・会員',
                'verbose_name_plural': '年会費・手数料・会員',
                'db_table': 'da_user_fee',
            },
        ),
    ]
