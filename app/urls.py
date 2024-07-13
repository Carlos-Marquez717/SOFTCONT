# en trabajadores/urls.py
from django.urls import path
from django.contrib.auth.views import logout_then_login
from .views import registrar_trabajador,lista_trabajador,registro_empresa,lista_empresa,eliminar,registro_obrero,lista_obrero,eliminar_obrero,registro_pedido,lista_pedido,eliminar_pedido,lista_pedido_trabajador,registro_material,eliminar_material,lista_material,editar_material,editar_obrero,editar_empresa,editar_pedido,home,registro_Herramienta,lista_Herramienta,editar_herramienta,eliminar_herramienta,lista_prestamo,registrar_prestamo,editar_prestamo,lista_prestamos_obrero,registro_Repuesto,eliminar_repuesto,lista_Repuesto,editar_Repuesto,registro_RetiroRepuesto,lista_RetiroRepuesto,eliminar_RetiroRepuesto,editar_RetiroRepuesto,lista_RetiroRepuesto_obrero,login,logout,generar_pdf_pedido,generar_pdf_pedidos,generar_pdf_prestamos,generar_pdf_prestamo,lista_utilesaseo,registro_utilesaseo,generar_pdf_utiles_aseo,registro_pedido_success,registro_prestamo_success,registro_RetiroRepuesto_success,generar_pdf_retiro,generar_pdf_retiros_general

urlpatterns = [
    path('login/', login, name='login' ),
    path('logout/', logout_then_login, name='logout'),

    path('registrar/', registrar_trabajador, name='registrar_trabajador'),
    path('listar/', lista_trabajador, name='lista_trabajador'),
    path('registro_empresa/', registro_empresa, name='registro_empresa'),
    path('lista_empresa/', lista_empresa, name='lista_empresa'),
    path('eliminar/<id>/', eliminar, name='eliminar' ),
    path('editar_empresa/<int:empresa_id>/', editar_empresa, name='editar_empresa'),
    path('eliminar_obrero/<id>/', eliminar_obrero, name='eliminar_obrero' ),
    path('registro_obrero/', registro_obrero, name='registro_obrero'),
    path('lista_obrero/', lista_obrero, name='lista_obrero'),
    path('editar_obrero/<int:obrero_id>/', editar_obrero, name='editar_obrero'),

    path('registro_pedido/', registro_pedido, name='registro_pedido'),
    path('registro_pedido/success/', registro_pedido_success, name='registro_pedido_success'),
    path('registro_prestamo/success', registro_prestamo_success, name='registro_prestamo_success'),
    path('lista_pedido/', lista_pedido, name='lista_pedido'),
    path('lista_pedido_trabajador/<int:trabajador_id>/', lista_pedido_trabajador, name='lista_pedido_trabajador'),
    path('eliminar_pedido/<int:pedido_id>/', eliminar_pedido, name='eliminar_pedido'),
    path('editar_pedido/<int:pedido_id>/', editar_pedido, name='editar_pedido'),

    path('registro_material/', registro_material, name='registro_material'),
    path('lista_material/', lista_material, name='lista_material'),
    path('eliminar_material/<int:material_id>/', eliminar_material, name='eliminar_material'),
    path('editar_material/<int:material_id>/', editar_material, name='editar_material'),
    path('registro_Herramienta/', registro_Herramienta, name='registro_Herramienta'),
    path('lista_Herramienta/', lista_Herramienta, name='lista_Herramienta'),
    path('editar_herramienta/<int:id>/', editar_herramienta, name='editar_herramienta'),
    path('eliminar_herramienta/<id>/', eliminar_herramienta, name='eliminar_herramienta' ),
    path('lista_prestamo/', lista_prestamo, name='lista_prestamo'),
    path('registrar_prestamo/', registrar_prestamo, name='registrar_prestamo'),
    path('editar_prestamo/<int:prestamo_id>/', editar_prestamo, name='editar_prestamo'),
    path('lista_prestamos_obrero/<int:obrero_id>/', lista_prestamos_obrero, name='lista_prestamos_obrero'),
    path('registro_Repuesto/', registro_Repuesto, name='registro_Repuesto'),
    path('eliminar_repuesto/<int:id>/', eliminar_repuesto, name='eliminar_repuesto'),
    path('lista_Repuesto/', lista_Repuesto, name='lista_Repuesto'),
    path('editar_Repuesto/<int:repuesto_id>/', editar_Repuesto, name='editar_Repuesto'),

    path('registro_RetiroRepuesto/', registro_RetiroRepuesto, name='registro_RetiroRepuesto'),
    path('registro_RetiroRepuesto/success', registro_RetiroRepuesto_success, name='registro_RetiroRepuesto_success'),
    path('lista_RetiroRepuesto/', lista_RetiroRepuesto, name='lista_RetiroRepuesto'),
    path('eliminar_RetiroRepuesto/<int:id>/', eliminar_RetiroRepuesto, name='eliminar_RetiroRepuesto'),
    path('editar_RetiroRepuesto/<int:retirorepuesto_id>/', editar_RetiroRepuesto, name='editar_RetiroRepuesto'),
    path('lista_RetiroRepuesto_obrero/<int:obrero_id>/', lista_RetiroRepuesto_obrero, name='lista_RetiroRepuesto_obrero'),
    path('generar_pdf_retiro/<int:obrero_id>/', generar_pdf_retiro, name='generar_pdf_retiro'),
     path('generar_pdf_retiros_general/', generar_pdf_retiros_general, name='generar_pdf_retiros_general'),

    path('', home, name='home'),

    path('generar_pdf_pedido/<int:obrero_id>/', generar_pdf_pedido, name='generar_pdf_pedido'),  
    path('generar_pdf_pedidos/', generar_pdf_pedidos, name='generar_pdf_pedidos'),
    path('generar_pdf_prestamos/', generar_pdf_prestamos, name='generar_pdf_prestamos'),
    path('generar_pdf_prestamo/<int:obrero_id>/', generar_pdf_prestamo, name='generar_pdf_prestamo'),
    # Puedes agregar más rutas aquí según sea necesario

    path('lista_utilesaseo/', lista_utilesaseo, name='lista_utilesaseo'),
    path('registro_utilesaseo/', registro_utilesaseo, name='registro_utilesaseo'), 
    path('generar_pdf_utiles_aseo/', generar_pdf_utiles_aseo, name='generar_pdf_utiles_aseo'),


]


