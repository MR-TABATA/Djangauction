# Generated by Django 4.2.3 on 2023-10-06 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pathxgroup',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='pathxgroup',
            name='path_id',
        ),
        migrations.DeleteModel(
            name='Path',
        ),
        migrations.DeleteModel(
            name='PathXGroup',
        ),
    ]
