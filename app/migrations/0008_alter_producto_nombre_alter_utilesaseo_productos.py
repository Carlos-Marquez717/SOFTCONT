# Generated by Django 5.0.1 on 2024-08-11 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_producto_remove_utilesaseo_producto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='utilesaseo',
            name='productos',
            field=models.ManyToManyField(related_name='utilesaseos', to='app.producto', verbose_name='Producto'),
        ),
    ]
