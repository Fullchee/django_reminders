# Generated by Django 3.2.3 on 2022-04-24 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_link_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='start_time_in_sec',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='link',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]
