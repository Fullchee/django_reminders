# Generated by Django 3.2.3 on 2021-08-01 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_link_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='flag',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
