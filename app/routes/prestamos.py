from django.urls import path

from app import views

urlpatterns = [
    path("registro_prestamo/success", views.registro_prestamo_success, name="registro_prestamo_success"),
    path("lista_prestamo/", views.lista_prestamo, name="lista_prestamo"),
    path("registrar_prestamo/", views.registrar_prestamo, name="registrar_prestamo"),
    path("editar_prestamo/<int:prestamo_id>/", views.editar_prestamo, name="editar_prestamo"),
    path(
        "lista_prestamos_obrero/<int:obrero_id>/",
        views.lista_prestamos_obrero,
        name="lista_prestamos_obrero",
    ),
]
