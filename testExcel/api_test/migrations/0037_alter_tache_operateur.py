# Generated by Django 3.2 on 2021-06-08 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0036_alter_tache_operateur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tache',
            name='operateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_test.operateur'),
        ),
    ]
