# en trabajadores/models.py
from django.db import models


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
    area = models.CharField(max_length=100,verbose_name="AREA")
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido-{self.id}"



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

