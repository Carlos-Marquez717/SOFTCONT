# en registro_trabajadores/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView,logout_then_login



urlpatterns = [
    path('Admin/', admin.site.urls),
    path('',include ('app.apps.AppConfig.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='Registration/login.html')),
    path('logout/', logout_then_login, name='logout'),
    
  

    
    # Puedes agregar más rutas aquí según sea necesario
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
