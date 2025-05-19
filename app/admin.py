from django.contrib import admin
from .models import (
    Empresa, Obrero, Material, Trabajador, Pedido, Herramienta, 
    Prestamo, Repuesto, RetiroRepuesto, Utilesaseo, Producto, congelado, PedidoInsumo
)

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
