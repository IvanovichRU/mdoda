from django import template
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from manejador.Colecciones.Tema import Tema
from django.template import loader

# Create your views here.
def index(request):
    plantilla = loader.get_template('manejador/index.html')
    return HttpResponse(plantilla.render({}, request))

def buscar_tema(request):
    plantila = loader.get_template('manejador/buscar_temas.html')
    tema_a_buscar = request.POST['tema_a_buscar']
    if (tema_a_buscar == ""):
        contexto = {'temas': Tema.todos()}
    else:
        contexto = {'temas': Tema.buscar(tema_a_buscar)}
    return HttpResponse(plantila.render(contexto, request))

def agregar_tema(request):
    tema_texto = request.POST['tema_a_agregar']
    tema_a_agregar = Tema(tema_texto)
    tema_a_agregar.guardar()
    return HttpResponseRedirect('/')