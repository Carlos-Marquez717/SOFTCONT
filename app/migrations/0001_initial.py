# Generated by Django 5.0.1 on 2024-01-26 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Herramienta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Obrero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Repuesto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(verbose_name='CANTIDAD')),
                ('area', models.CharField(max_length=100, verbose_name='AREA')),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('compañia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pedido', to='app.empresa', verbose_name='EMPRESA')),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pedido', to='app.material', verbose_name='INSUMO')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido', to='app.obrero', verbose_name='OBRERO')),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ENTREGADO', 'Entregado'), ('NO_ENTREGADO', 'No Entregado')], default='NO_ENTREGADO', max_length=20)),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('fecha_recepcion', models.DateField(blank=True, null=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestamo', to='app.empresa', verbose_name='empresa')),
                ('herramienta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestamo', to='app.herramienta', verbose_name='Herramienta')),
                ('nombre_solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestamo', to='app.obrero', verbose_name='Obrero')),
            ],
        ),
        migrations.CreateModel(
            name='RetiroRepuesto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('fecha_retiro', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RetiroRepuesto', to='app.empresa', verbose_name='empresa')),
                ('nombre_solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RetiroRepuesto', to='app.obrero', verbose_name='Obrero')),
                ('repuesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RetiroRepuesto', to='app.repuesto', verbose_name='Herramienta')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Trabajador', to='app.empresa', verbose_name='empresa o grupo')),
                ('nombre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Trabajador', to='app.obrero', verbose_name='Obrero')),
            ],
        ),
    ]
