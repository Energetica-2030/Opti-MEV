# Generated by Django 4.2 on 2023-04-22 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viability', '0005_alter_vehicle_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='combustion_autonomy',
            new_name='fuel_autonomy',
        ),
    ]