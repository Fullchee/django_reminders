# Generated by Django 3.2.3 on 2021-06-08 01:02

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_link_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='link',
            name='last_accessed',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2021, 6, 8, 1, 2, 20, 994315)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='link',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
