from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buscar_tema', views.buscar_tema, name='buscar_tema')
]