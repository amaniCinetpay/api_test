# Generated by Django 3.2 on 2021-05-24 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0026_auto_20210524_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trxnonereconciled',
            name='AmountCorrespodent',
        ),
        migrations.RemoveField(
            model_name='trxnonereconciled',
            name='StautTransactionCorrespondent',
        ),
        migrations.RemoveField(
            model_name='trxnonereconciled',
            name='cel_phone_numCorrespondant',
        ),
        migrations.RemoveField(
            model_name='trxnonereconciled',
            name='cpm_trans_idCorrespondent',
        ),
        migrations.RemoveField(
            model_name='trxnonereconciled',
            name='created_atCorrespondent',
        ),
        migrations.RemoveField(
            model_name='trxnonereconciled',
            name='payment_methodCorrespondant',
        ),
    ]