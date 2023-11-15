# Generated by Django 4.2.3 on 2023-10-24 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_apply_mail_apply_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='生成日時')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='削除日時')),
                ('subject', models.CharField(blank=True, max_length=100, null=True, verbose_name='メールタイトル')),
                ('body', models.CharField(blank=True, max_length=100, null=True, verbose_name='メール本文')),
                ('to', models.CharField(blank=True, max_length=100, null=True, verbose_name='宛先')),
                ('bcc', models.CharField(blank=True, max_length=100, null=True, verbose_name='BCC')),
            ],
            options={
                'verbose_name': 'メールオプション情報',
                'verbose_name_plural': 'メールオプション情報',
                'db_table': 'da_mail',
            },
        ),
    ]
