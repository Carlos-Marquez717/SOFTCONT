from django.contrib import admin
from .models import (
    Empresa, Obrero, Material, Trabajador, Pedido, Herramienta, 
    Prestamo, Repuesto, RetiroRepuesto, Utilesaseo, Producto, congelado, PedidoInsumo, Informe
)
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ImagenInforme
import os

# Admin de Repuesto
@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'ubicacion')

# Admin de RetiroRepuesto
@admin.register(RetiroRepuesto)
class RetiroRepuestoAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'empresa', 'repuesto', 'cantidad', 'fecha_retiro', 'area')

# Inline de PedidoInsumo
class PedidoInsumoInline(admin.TabularInline):
    model = PedidoInsumo
    extra = 1
    fields = ['insumos', 'cantidad']

# Admin de Pedido
class PedidoAdmin(admin.ModelAdmin):
    inlines = [PedidoInsumoInline]
    list_display = ('solicitante', 'compañia', 'area', 'fecha_pedido')
    search_fields = ('solicitante__nombre', 'compañia__nombre', 'area')
    fields = ['solicitante', 'compañia', 'area', 'fecha_pedido']

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        pedido = form.instance

        for instance in instances:
            try:
                # Si el solicitante es un Obrero, busca el Trabajador correspondiente
                if isinstance(pedido.solicitante, Obrero):
                    trabajador = Trabajador.objects.get(obrero=pedido.solicitante)
                elif isinstance(pedido.solicitante, Trabajador):
                    trabajador = pedido.solicitante
                else:
                    trabajador = None

                if trabajador is not None:
                    instance.trabajador = trabajador
                    instance.empresa = pedido.compañia
                    instance.save()
                else:
                    # Si no se puede encontrar un trabajador válido, no se guarda la instancia
                    continue

            except Trabajador.DoesNotExist:
                # Podrías loggear el error o mostrar un mensaje
                continue

        formset.save_m2m()

# Admin de PedidoInsumo
class PedidoInsumoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'insumos', 'cantidad']
    list_filter = ['pedido']

# Admin de Informe
@admin.register(Informe)
class InformeAdmin(admin.ModelAdmin):
    list_display = ('id', 'caso', 'area', 'hora_inicio', 'hora_culm', 'fecha', 'imagen_antes', 'imagen_despues')
    search_fields = ('descripcion',)
    list_filter = ('caso', 'fecha')

    def delete_model(self, request, obj):
        # Elimina imágenes asociadas en disco
        for imagen in obj.imagenes.all():
            if imagen.imagen and os.path.isfile(imagen.imagen.path):
                os.remove(imagen.imagen.path)
        # Elimina imágenes antes/después si existen
        if obj.imagen_antes and os.path.isfile(obj.imagen_antes.path):
            os.remove(obj.imagen_antes.path)
        if obj.imagen_despues and os.path.isfile(obj.imagen_despues.path):
            os.remove(obj.imagen_despues.path)
        super().delete_model(request, obj)

# Eliminar archivos de ImagenInforme al borrar desde cualquier lugar
@receiver(post_delete, sender=ImagenInforme)
def eliminar_archivo_imagen(sender, instance, **kwargs):
    if instance.imagen and os.path.isfile(instance.imagen.path):
        os.remove(instance.imagen.path)

# Eliminar archivos de imagen_antes y imagen_despues al borrar Informe desde cualquier lugar
@receiver(post_delete, sender=Informe)
def eliminar_imagenes_informe(sender, instance, **kwargs):
    if instance.imagen_antes and os.path.isfile(instance.imagen_antes.path):
        os.remove(instance.imagen_antes.path)
    if instance.imagen_despues and os.path.isfile(instance.imagen_despues.path):
        os.remove(instance.imagen_despues.path)

# Registro de modelos
admin.site.register(PedidoInsumo, PedidoInsumoAdmin)
admin.site.register(Empresa)
admin.site.register(Obrero)
admin.site.register(Material)
admin.site.register(Trabajador)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Herramienta)
admin.site.register(Prestamo)
admin.site.register(Utilesaseo)
admin.site.register(Producto)
admin.site.register(congelado)
