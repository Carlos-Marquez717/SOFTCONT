from django.contrib import admin
from .models import Empresa, Obrero, Material, Trabajador, Pedido, Herramienta, Prestamo, Repuesto, RetiroRepuesto , Utilesaseo, Producto

# Registrar cada modelo en el admin
admin.site.register(Empresa)
admin.site.register(Obrero)
admin.site.register(Material)
admin.site.register(Trabajador)
admin.site.register(Pedido)
admin.site.register(Herramienta)
admin.site.register(Prestamo)
admin.site.register(Repuesto)
admin.site.register(RetiroRepuesto)
admin.site.register(Utilesaseo)
admin.site.register(Producto)
