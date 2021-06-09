# Generated by Django 3.2 on 2021-05-23 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0010_auto_20210524_0003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trxreconciled',
            old_name='cpm_payment_date',
            new_name='account',
        ),
        migrations.AddField(
            model_name='trxreconciled',
            name='payment_date',
            field=models.CharField(default=-1.0, max_length=200),
            preserve_default=False,
        ),
    ]