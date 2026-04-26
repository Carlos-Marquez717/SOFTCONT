from django.contrib.auth.views import logout_then_login
from django.urls import path

from app import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("logout/", logout_then_login, name="logout"),
]
