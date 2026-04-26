from django.urls import path

from app import views

urlpatterns = [
    path("registrar/", views.registrar_trabajador, name="registrar_trabajador"),
    path("listar/", views.lista_trabajador, name="lista_trabajador"),
    path("registro_obrero/", views.registro_obrero, name="registro_obrero"),
    path("lista_obrero/", views.lista_obrero, name="lista_obrero"),
    path("eliminar_obrero/<id>/", views.eliminar_obrero, name="eliminar_obrero"),
    path("editar_obrero/<int:obrero_id>/", views.editar_obrero, name="editar_obrero"),
]
