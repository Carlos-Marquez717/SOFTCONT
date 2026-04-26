from django.urls import path

from app import views

urlpatterns = [
    path("registro_material/", views.registro_material, name="registro_material"),
    path("lista_material/", views.lista_material, name="lista_material"),
    path("eliminar_material/<int:material_id>/", views.eliminar_material, name="eliminar_material"),
    path("editar_material/<int:material_id>/", views.editar_material, name="editar_material"),
    path("registro_Herramienta/", views.registro_Herramienta, name="registro_Herramienta"),
    path("lista_Herramienta/", views.lista_Herramienta, name="lista_Herramienta"),
    path("editar_herramienta/<int:id>/", views.editar_herramienta, name="editar_herramienta"),
    path("eliminar_herramienta/<id>/", views.eliminar_herramienta, name="eliminar_herramienta"),
]
