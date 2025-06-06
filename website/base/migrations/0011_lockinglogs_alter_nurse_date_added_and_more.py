# Generated by Django 4.2.18 on 2025-05-11 13:06

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_patient_color_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='LockingLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nurse_id', models.BigIntegerField(default=None, null=True)),
                ('created_at', models.DateTimeField(default=base.models.local_timezone)),
                ('logs', models.CharField(blank=True, default=None, max_length=200, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='nurse',
            name='date_added',
            field=models.DateTimeField(default=base.models.local_timezone),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_added',
            field=models.DateTimeField(default=base.models.local_timezone),
        ),
    ]
