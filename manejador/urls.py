from django.urls import path

from . import views

urlpatterns = [
    path('login', views.vista_login, name='login'),
    path('buscar_objetos', views.buscar_objetos, name='buscar_objetos')
]