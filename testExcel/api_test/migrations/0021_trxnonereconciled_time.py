# Generated by Django 3.2 on 2021-05-24 09:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0020_remove_trxnonereconciled_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='trxnonereconciled',
            name='Time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 5, 24, 9, 4, 6, 483550, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
