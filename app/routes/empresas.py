from django.urls import path

from app import views

urlpatterns = [
    path("registro_empresa/", views.registro_empresa, name="registro_empresa"),
    path("lista_empresa/", views.lista_empresa, name="lista_empresa"),
    path("eliminar/<id>/", views.eliminar, name="eliminar"),
    path("editar_empresa/<int:empresa_id>/", views.editar_empresa, name="editar_empresa"),
]
