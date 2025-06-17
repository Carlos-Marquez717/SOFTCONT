from django.http import HttpResponseForbidden
from django.urls import resolve

ALLOWED_IP = '127.0.0.1'  # O la IP LAN de tu PC, por ejemplo: '192.168.1.20'
PUBLIC_PATHS = ['/verificar_reporte/', '/static/']  # Añade aquí tus rutas de verificación

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Permitir acceso a rutas públicas
        path = request.path
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return self.get_response(request)

        # Permitir acceso solo desde IP autorizada
        ip = request.META.get('REMOTE_ADDR')
        if ip != ALLOWED_IP:
            return HttpResponseForbidden("<h1>Acceso no permitido</h1>")

        return self.get_response(request)
