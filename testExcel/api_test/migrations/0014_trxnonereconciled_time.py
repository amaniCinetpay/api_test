# Generated by Django 3.2 on 2021-05-24 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0013_auto_20210524_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='trxnonereconciled',
            name='Time',
            field=models.DateTimeField(auto_now_add=True, default=-1.0),
            preserve_default=False,
        ),
    ]