from django.urls import path

from . import views

urlpatterns = [
    path('login', views.vista_login, name='login'),
    path('buscar_objetos', views.buscar_objetos, name='buscar_objetos'),
    path('obtener_objetos', views.obtener_objetos, name='obtener_objetos'),
    path('registrar_objeto', views.registrar_objeto, name='registrar_objeto'),
    path('arreglar_csrf', views.arreglar_csrf, name='arreglar_csrf'),
    path('perfil', views.refrescar_usuario, name='refrescar_usuario')
]