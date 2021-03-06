from django.urls import path

from . import views

urlpatterns = [
    path('login', views.vista_login, name='login'),
    path('buscar_objetos', views.buscar_objetos, name='buscar_objetos'),
    path('obtener_objetos', views.obtener_objetos, name='obtener_objetos'),
    path('obtener_info_objeto', views.obtener_info_objeto, name='obtener_info_objeto'),
    path('descargar_objeto', views.descargar_objeto, name='descargar_objeto'),
    path('registrar_objeto', views.registrar_objeto, name='registrar_objeto'),
    path('nuevo_usuario', views.nuevo_usuario, name='nuevo_usuario'),
    path('arreglar_csrf', views.arreglar_csrf, name='arreglar_csrf'),
    path('perfil', views.refrescar_usuario, name='refrescar_usuario')
]