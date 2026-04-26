from django.urls import path

from app import views

urlpatterns = [
    path("generar_pdf_pedido/<int:obrero_id>/", views.generar_pdf_pedido, name="generar_pdf_pedido"),
    path("generar_pdf_pedidos/", views.generar_pdf_pedidos, name="generar_pdf_pedidos"),
    path("generar_pdf_prestamos/", views.generar_pdf_prestamos, name="generar_pdf_prestamos"),
    path("generar_pdf_prestamo/<int:obrero_id>/", views.generar_pdf_prestamo, name="generar_pdf_prestamo"),
    path("generar_pdf_utiles_aseo/", views.generar_pdf_utiles_aseo, name="generar_pdf_utiles_aseo"),
    path("generar_pdf_retiro/<int:obrero_id>/", views.generar_pdf_retiro, name="generar_pdf_retiro"),
    path("generar_pdf_retiros_general/", views.generar_pdf_retiros_general, name="generar_pdf_retiros_general"),
    path("upload/", views.upload_csv, name="upload_csv"),
    path("lista/", views.lista_congelado, name="lista_congelado"),
    path("botones/", views.pagina_con_botones, name="pagina_con_botones"),
    path("generate_pdf/", views.generate_pdf, name="generate_pdf"),
    path("generate_pdf/personal/<str:personal>/", views.generate_pdf, name="generate_pdf_by_personal"),
    path("generate_pdf/empresa/<str:empresa>/", views.generate_pdf, name="generate_pdf_by_empresa"),
]
