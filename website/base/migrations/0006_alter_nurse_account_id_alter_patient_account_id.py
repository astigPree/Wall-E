# Generated by Django 4.2.11 on 2025-01-17 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_account_user_id_nurse_account_id_patient_account_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nurse',
            name='account_id',
            field=models.BigIntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='account_id',
            field=models.BigIntegerField(default=None, null=True),
        ),
    ]
