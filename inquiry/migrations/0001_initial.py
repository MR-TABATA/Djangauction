# Generated by Django 4.2.3 on 2023-09-24 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DAInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名前')),
                ('mail', models.EmailField(max_length=200, verbose_name='メールアドレス')),
                ('title', models.CharField(max_length=100, verbose_name='タイトル')),
                ('contents', models.CharField(max_length=1000, verbose_name='問い合わせ内容')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='生成日時')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='削除日時')),
            ],
            options={
                'verbose_name': '問い合わせ',
                'verbose_name_plural': '問い合わせ',
                'db_table': 'da_inquiry',
            },
        ),
    ]
