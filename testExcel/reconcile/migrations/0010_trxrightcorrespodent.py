# Generated by Django 3.2 on 2021-05-07 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reconcile', '0009_trxcorrespondent'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrxRightCorrespodent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datePaiement', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=200)),
                ('montant', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('creationCorrespondent', models.CharField(max_length=200)),
                ('TelephoneCorrespondant', models.CharField(max_length=200)),
                ('AmountCorrespodent', models.CharField(max_length=200)),
                ('methodePaimentCorrespondant', models.CharField(max_length=200)),
                ('StautTransactionCorrespondent', models.CharField(max_length=200)),
            ],
        ),
    ]
