# en trabajadores/models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.postgres.fields import ArrayField 


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
        return f"{self.solicitante.nombre} - {self.compañia.nombre} - {self.insumo.nombre} - {self.cantidad} - {self.area} - {self.fecha_pedido} "

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

    def __str__(self):
        return f"{self.nombre_solicitante.nombre} - {self.empresa.nombre} - {self.herramienta.nombre} - {self.status} - {self.fecha_creacion}"


class Repuesto(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre
    


class RetiroRepuesto(models.Model):
    trabajador = models.ForeignKey(Obrero, related_name="retirorepuesto", on_delete=models.CASCADE, verbose_name="Obrero")
    empresa = models.ForeignKey(Empresa, related_name="retirorepuesto", on_delete=models.CASCADE, verbose_name="empresa")
    repuesto = models.ForeignKey(Repuesto, related_name="retirorepuesto", on_delete=models.CASCADE, verbose_name="REPUESTO")
    cantidad = models.PositiveIntegerField()
    fecha_retiro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.trabajador} - {self.repuesto} - {self.cantidad}'




    



from django.core.exceptions import ValidationError


class Producto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre





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

  

    mes = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ENERO')
    productos = models.ManyToManyField('Producto', related_name='utilesaseos', verbose_name="Producto")
    cantidad = models.PositiveIntegerField()
    fecha_creacion = models.DateField(auto_now_add=True)
    nombre_solicitante = models.ForeignKey('Obrero', related_name="utilesaseo", on_delete=models.CASCADE, verbose_name="Obrero")
    empresa = models.ForeignKey('Empresa', related_name="utilesaseo", on_delete=models.CASCADE, verbose_name="empresa")
    run = models.CharField(max_length=100)

    def clean(self):
        # Obtener el mes actual y el año actual
        now = datetime.now()
        current_year = now.year

        # Verificar registros existentes
        same_month_records = Utilesaseo.objects.filter(
            mes=self.mes,
            fecha_creacion__year=current_year,
            nombre_solicitante=self.nombre_solicitante,
            empresa=self.empresa
        )

        if same_month_records.count() >= 3:
            raise ValidationError(f'Ya existen 3 registros para el mes {self.get_mes_display()} en el año actual. Para el Trabajador')

        # Después de guardar el objeto, puedes verificar las relaciones ManyToMany
        if self.pk:  # Solo si el objeto ya tiene un ID
            for producto in self.productos.all():
                same_month_product_records = same_month_records.filter(productos=producto)
                if same_month_product_records.exists():
                    raise ValidationError(f'Ya existe un registro para el mes {self.get_mes_display()} y el producto {producto.nombre} en el año actual. Para el Trabajador')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Guardar la relación ManyToMany después de guardar el objeto principal
        self.productos.set(self.productos.all())

    def __str__(self):
        productos_nombres = ", ".join([producto.nombre for producto in self.productos.all()])
        return f"{self.mes} - {productos_nombres} - {self.cantidad}"






class congelado(models.Model):
    orden= models.IntegerField()
    caso=models.CharField(max_length=30, null=True, blank=True)
    tag=models.CharField(max_length=30)
    descripcion_de_equipo=models.CharField(max_length=30)
    Descripcion_del_fallo=models.CharField(max_length=30)
    personal=models.CharField(max_length=80)
    fecha_de_inicio=models.DateField()
    especialidad=models.CharField(max_length=80)
    empresa=models.CharField(max_length=80)
    turno=models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.orden} - {self.caso} - {self.tag} - {self.personal} - {self.fecha_de_inicio} - {self.turno}"