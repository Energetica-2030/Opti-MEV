# Generated by Django 4.2 on 2023-04-21 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viability', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='type',
            field=models.CharField(choices=[(0, 'Eléctrico'), (1, 'Híbrido')], default='Eléctrico', max_length=20),
        ),
    ]