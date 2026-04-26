from django.urls import path

from app import views

urlpatterns = [
    path("registro_Repuesto/", views.registro_Repuesto, name="registro_Repuesto"),
    path("eliminar_repuesto/<int:id>/", views.eliminar_repuesto, name="eliminar_repuesto"),
    path("lista_Repuesto/", views.lista_Repuesto, name="lista_Repuesto"),
    path("editar_Repuesto/<int:repuesto_id>/", views.editar_Repuesto, name="editar_Repuesto"),
    path("registro_RetiroRepuesto/", views.registro_RetiroRepuesto, name="registro_RetiroRepuesto"),
    path(
        "registro_RetiroRepuesto/success",
        views.registro_RetiroRepuesto_success,
        name="registro_RetiroRepuesto_success",
    ),
    path("lista_RetiroRepuesto/", views.lista_RetiroRepuesto, name="lista_RetiroRepuesto"),
    path("eliminar_RetiroRepuesto/<int:id>/", views.eliminar_RetiroRepuesto, name="eliminar_RetiroRepuesto"),
    path(
        "editar_RetiroRepuesto/<int:retirorepuesto_id>/",
        views.editar_RetiroRepuesto,
        name="editar_RetiroRepuesto",
    ),
    path(
        "lista_RetiroRepuesto_obrero/<int:obrero_id>/",
        views.lista_RetiroRepuesto_obrero,
        name="lista_RetiroRepuesto_obrero",
    ),
]
