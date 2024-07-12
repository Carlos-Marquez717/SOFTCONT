# en trabajadores/models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime


class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
 

    def __str__(self):
        return self.nombre
    
class Obrero(models.Model):
    nombre = models.CharField(max_length=100)
 

    def __str__(self):
        return self.nombre    
    
class Material(models.Model):
    nombre = models.CharField(max_length=100)
 

    def __str__(self):
        return self.nombre
        

class Trabajador(models.Model):
    nombre = models.ForeignKey(Obrero, related_name="Trabajador",on_delete=models.CASCADE, verbose_name="Obrero")
    empresa = models.ForeignKey(Empresa, related_name="Trabajador",on_delete=models.CASCADE, verbose_name="empresa o grupo")

    def __str__(self):
        return self.nombre
    

class Pedido(models.Model):
    solicitante = models.ForeignKey(Obrero, related_name="pedido", on_delete=models.CASCADE, verbose_name="OBRERO")
    compañia = models.ForeignKey(Empresa, related_name="Pedido", on_delete=models.CASCADE, verbose_name="EMPRESA")
    insumo = models.ForeignKey(Material, related_name="Pedido", on_delete=models.CASCADE, verbose_name="INSUMO")
    cantidad = models.IntegerField(verbose_name="CANTIDAD")
    area = models.CharField(max_length=100, verbose_name="AREA")
    fecha_pedido = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Pedido-{self.id}"

    def fecha_pedido_formatted(self):
        return self.fecha_pedido.strftime("%d/%m/%Y %H:%M")



class Herramienta(models.Model):
    nombre = models.CharField(max_length=100)
 

    def __str__(self):
        return self.nombre    
    

class Prestamo(models.Model):
    STATUS_CHOICES = [
        ('ENTREGADO', 'Entregado'),
        ('NO_ENTREGADO', 'No Entregado'),
    ]

    nombre_solicitante = models.ForeignKey(Obrero, related_name="prestamo", on_delete=models.CASCADE, verbose_name="Obrero")
    empresa = models.ForeignKey(Empresa, related_name="prestamo", on_delete=models.CASCADE, verbose_name="empresa")
    herramienta = models.ForeignKey(Herramienta, related_name="prestamo", on_delete=models.CASCADE, verbose_name="Herramienta")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NO_ENTREGADO')
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_recepcion = models.DateField(null=True, blank=True)    

class Repuesto(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    def __str__(self):
        return self.nombre  
    


class RetiroRepuesto(models.Model):
    trabajador = models.ForeignKey(Obrero, related_name="retirorepuesto", on_delete=models.CASCADE, verbose_name="Obrero")
    empresa = models.ForeignKey(Empresa, related_name="retirorepuesto", on_delete=models.CASCADE, verbose_name="empresa")
    repuesto = models.ForeignKey(Repuesto, related_name="retirorepuesto", on_delete=models.CASCADE, verbose_name="REPUESTO")
    cantidad = models.PositiveIntegerField()
    fecha_retiro = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Actualizar la cantidad de repuestos al realizar un retiro
        self.repuesto.cantidad -= self.cantidad
        self.repuesto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.trabajador} - {self.repuesto.nombre}'



class Utilesaseo(models.Model):
    STATUS_CHOICES = [
        ('ENERO', 'ENERO'),
        ('FEBRERO', 'FEBRERO'),
        ('MARZO', 'MARZO'),
        ('ABRIL', 'ABRIL'),
        ('MAYO', 'MAYO'),
        ('JUNIO', 'JUNIO'),
        ('JULIO', 'JULIO'),
        ('AGOSTO', 'AGOSTO'),
        ('SEPTIEMBRE', 'SEPTIEMBRE'),
        ('OCTUBRE', 'OCTUBRE'),
        ('NOVIEMBRE', 'NOVIEMBRE'),
        ('DICIEMBRE', 'DICIEMBRE'),
    ]

    STATUS_CHOICES1 = [
        ('OMO', 'OMO'),
        ('JABON', 'JABON'),
        ('CONFORT', 'CONFORT'),
    ]

    mes = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ENERO')
    producto = models.CharField(max_length=20, choices=STATUS_CHOICES1, default='OMO')
    cantidad = models.PositiveIntegerField()
    fecha_creacion = models.DateField(auto_now_add=True)
    nombre_solicitante = models.ForeignKey(Obrero, related_name="utilesaseo", on_delete=models.CASCADE, verbose_name="Obrero")
    empresa = models.ForeignKey(Empresa, related_name="utilesaseo", on_delete=models.CASCADE, verbose_name="empresa")
    run = models.CharField(max_length=100)

    def clean(self):
        # Obtener el mes actual y el año actual
        now = datetime.now()
        current_year = now.year

        # Contar cuántos registros existen para este mes y año
        same_month_records = Utilesaseo.objects.filter(
            mes=self.mes,
            fecha_creacion__year=current_year,
            nombre_solicitante=self.nombre_solicitante,
            empresa=self.empresa
        )

        # Contar cuántos registros existen para este mes y producto específico ('OMO', 'JABON', 'CONFORT')
        same_month_product_records = same_month_records.filter(producto=self.producto)

        # Verificar si ya existe un registro para este mes y año
        if same_month_records.count() >= 3:
            raise ValidationError(f'Ya existen 3 registros para el mes {self.get_mes_display()} en el año actual.Para el Trabajador')

        # Verificar si ya existe un registro para este mes y producto específico ('OMO', 'JABON', 'CONFORT')
        if self.producto in dict(self.STATUS_CHOICES1).keys() and same_month_product_records.exists():
            raise ValidationError(f'Ya existe un registro para el mes {self.get_mes_display()} y el producto {self.get_producto_display()} en el año actual. Para el Trabajador')

    def save(self, *args, **kwargs):
        # Asegurar que fecha_creacion se establezca adecuadamente si no se proporciona al crear una nueva instancia de Utilesaseo
        if not self.fecha_creacion:
            self.fecha_creacion = datetime.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Utilesaseo - {self.id}"



