# Generated by Django 4.2.18 on 2025-02-01 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_patient_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='color_location',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
