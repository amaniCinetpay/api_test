# Generated by Django 3.2 on 2021-05-05 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reconcile', '0005_auto_20210504_1220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trxoperateur',
            old_name='date',
            new_name='datepaiment',
        ),
        migrations.RenameField(
            model_name='trxoperateur',
            old_name='CompteOM',
            new_name='montant',
        ),
        migrations.RenameField(
            model_name='trxoperateur',
            old_name='correspondant',
            new_name='telephone',
        ),
        migrations.RemoveField(
            model_name='trxoperateur',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='trxoperateur',
            name='mode',
        ),
    ]