from django.urls import path

from app import views

urlpatterns = [
    path("registro_pedido/", views.registro_pedido, name="registro_pedido"),
    path("registro_pedido/success/", views.registro_pedido_success, name="registro_pedido_success"),
    path("lista_pedido/", views.lista_pedido, name="lista_pedido"),
    path(
        "lista_pedido_trabajador/<int:trabajador_id>/",
        views.lista_pedido_trabajador,
        name="lista_pedido_trabajador",
    ),
    path("eliminar_pedido/<int:pedido_id>/", views.eliminar_pedido, name="eliminar_pedido"),
    path("editar_pedido/<int:pedido_id>/", views.editar_pedido, name="editar_pedido"),
    path("pedidos_total/", views.pedidos_total, name="pedidos_total"),
    path("pedidos_semanales/", views.pedidos_semanales, name="pedidos_semanales"),
    path("pedidos_semana/", views.pedidos_semana, name="pedidos_semana"),
    path("pedidos_mes/", views.pedidos_mes, name="pedidos_mes"),
    path("pedidos-anio/", views.pedidos_anio, name="pedidos_anio"),
    path("pedidos_mensuales/", views.pedidos_mensuales, name="pedidos_mensuales"),
    path("pedidos_dia/", views.pedidos_dia, name="pedidos_dia"),
]
