from django.urls import path

from app import views

urlpatterns = [
    path("lista_utilesaseo/", views.lista_utilesaseo, name="lista_utilesaseo"),
    path("registro_utilesaseo/", views.registro_utilesaseo, name="registro_utilesaseo"),
]
