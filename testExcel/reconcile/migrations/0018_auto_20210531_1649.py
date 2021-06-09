# Generated by Django 3.2 on 2021-05-31 14:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reconcile', '0017_trxrightcorrespodent_idpaiment'),
    ]

    operations = [
        migrations.AddField(
            model_name='trxcinetpay',
            name='cpm_custom',
            field=models.CharField(default=-1.0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trxcorrespondent',
            name='cpm_custom',
            field=models.CharField(default=1.0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trxfailedcinetpay',
            name='cpm_custom',
            field=models.CharField(default=datetime.datetime(2021, 5, 31, 14, 49, 12, 233157, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trxrightcorrespodent',
            name='cpm_custom',
            field=models.CharField(default=datetime.datetime(2021, 5, 31, 14, 49, 16, 529085, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trxsuccesscinetpay',
            name='cpm_custom',
            field=models.CharField(default=datetime.datetime(2021, 5, 31, 14, 49, 19, 684110, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
