# Generated by Django 3.2.3 on 2021-05-30 15:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), null=True, size=None)),
                ('url', models.URLField(null=True)),
                ('notes', models.TextField(null=True)),
                ('last_accessed', models.DateField(auto_now_add=True, null=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('type', models.CharField(choices=[('POD', 'Podcast'), ('MUS', 'Music'), ('YT', 'YouTube')], max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('author', models.CharField(max_length=200)),
            ],
        ),
    ]
