# Generated by Django 3.2 on 2021-05-06 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reconcile', '0008_trxdifference_trxfailedcinetpay'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrxCorrespondent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(max_length=200)),
                ('datePaiement', models.CharField(max_length=200)),
                ('marchand', models.CharField(max_length=200)),
                ('EmailMarchand', models.CharField(max_length=200)),
                ('NomDuService', models.CharField(max_length=200)),
                ('IdTransaction', models.CharField(max_length=200)),
                ('SiteId', models.CharField(max_length=200)),
                ('Montant', models.CharField(max_length=200)),
                ('Devise', models.CharField(max_length=200)),
                ('methodePaiment', models.CharField(max_length=200)),
                ('Telephone', models.CharField(max_length=200)),
                ('EtatTransaction', models.CharField(max_length=200)),
                ('IdPaiment', models.CharField(max_length=200)),
            ],
        ),
    ]
