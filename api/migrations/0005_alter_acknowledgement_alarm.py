# Generated by Django 3.2.3 on 2021-06-27 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_acknowledgement_alarm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acknowledgement',
            name='alarm',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='ack', to='api.alarm'),
        ),
    ]