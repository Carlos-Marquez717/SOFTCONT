from django.urls import path

from .routes.auth import urlpatterns as auth_urlpatterns
from .routes.core import urlpatterns as core_urlpatterns
from .routes.empresas import urlpatterns as empresas_urlpatterns
from .routes.inventario import urlpatterns as inventario_urlpatterns
from .routes.pedidos import urlpatterns as pedidos_urlpatterns
from .routes.prestamos import urlpatterns as prestamos_urlpatterns
from .routes.reportes import urlpatterns as reportes_urlpatterns
from .routes.repuestos import urlpatterns as repuestos_urlpatterns
from .routes.trabajadores import urlpatterns as trabajadores_urlpatterns
from .routes.utiles_aseo import urlpatterns as utiles_aseo_urlpatterns

urlpatterns = [
    *auth_urlpatterns,
    *core_urlpatterns,
    *empresas_urlpatterns,
    *trabajadores_urlpatterns,
    *pedidos_urlpatterns,
    *inventario_urlpatterns,
    *prestamos_urlpatterns,
    *repuestos_urlpatterns,
    *utiles_aseo_urlpatterns,
    *reportes_urlpatterns,
]
