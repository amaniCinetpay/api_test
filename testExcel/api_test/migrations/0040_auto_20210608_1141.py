# Generated by Django 3.2 on 2021-06-08 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0039_auto_20210608_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='operateur',
            name='code',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tache',
            name='operateur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_test.operateur'),
        ),
    ]