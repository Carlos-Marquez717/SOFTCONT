# Generated by Django 5.0.1 on 2024-08-07 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_utilesaseo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilesaseo',
            name='mes',
            field=models.CharField(choices=[('ENERO', 'ENERO'), ('FEBRERO', 'FEBRERO'), ('MARZO', 'MARZO'), ('ABRIL', 'ABRIL'), ('MAYO', 'MAYO'), ('JUNIO', 'JUNIO'), ('JULIO', 'JULIO'), ('AGOSTO', 'AGOSTO'), ('SEPTIEMBRE', 'SEPTIEMBRE'), ('OCTUBRE', 'OCTUBRE'), ('NOVIEMBRE', 'NOVIEMBRE'), ('DICIEMBRE', 'DICIEMBRE')], default='ENERO', max_length=20),
        ),
    ]
