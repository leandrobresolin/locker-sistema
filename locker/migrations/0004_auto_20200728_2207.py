# Generated by Django 3.0.8 on 2020-07-28 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locker', '0003_auto_20200728_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='door_status',
            field=models.BooleanField(default=False),
        ),
    ]
