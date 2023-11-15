# Generated by Django 4.2.3 on 2023-09-27 12:25

import accounts.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, max_length=50, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('mobile', models.CharField(blank=True, max_length=20, verbose_name='携帯')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='名')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='姓')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='メール')),
                ('company', models.CharField(blank=True, max_length=100, verbose_name='会社名')),
                ('department', models.CharField(blank=True, max_length=100, verbose_name='所属')),
                ('position', models.CharField(blank=True, max_length=100, verbose_name='役職')),
                ('occupation', models.CharField(blank=True, max_length=100, verbose_name='職種')),
                ('avater', models.ImageField(upload_to=accounts.models.avater_file_path)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='生成日時')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='削除日時')),
                ('delete_memo', models.TextField(blank=True, null=True, verbose_name='削除理由')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalCustomUser',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, max_length=50, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('mobile', models.CharField(blank=True, max_length=20, verbose_name='携帯')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='名')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='姓')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='メール')),
                ('company', models.CharField(blank=True, max_length=100, verbose_name='会社名')),
                ('department', models.CharField(blank=True, max_length=100, verbose_name='所属')),
                ('position', models.CharField(blank=True, max_length=100, verbose_name='役職')),
                ('occupation', models.CharField(blank=True, max_length=100, verbose_name='職種')),
                ('avater', models.TextField(max_length=100)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created', models.DateTimeField(blank=True, editable=False, verbose_name='生成日時')),
                ('modified', models.DateTimeField(blank=True, editable=False, verbose_name='更新日時')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='削除日時')),
                ('delete_memo', models.TextField(blank=True, null=True, verbose_name='削除理由')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical user',
                'verbose_name_plural': 'historical users',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]