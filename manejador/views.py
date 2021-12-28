import json
from django.http.response import HttpResponse, JsonResponse
from manejador.Colecciones.Usuario import Usuario
from manejador.Colecciones.ObjetoDeAprendizaje import ObjetoDeAprendizaje
from django.template import loader

# Create your views here.
def vista_login(request):
    datos = json.loads(request.body)
    if 'token_sesion' in datos:
        usuario = Usuario.recuperar_sesion(datos['token_sesion'])
        if usuario is not None:
            dict_a_enviar = usuario.__dict__
            dict_a_enviar.pop('contraseña')
            dict_a_enviar['_id'] = str(dict_a_enviar['_id'])
            return JsonResponse ({'Usuario': dict_a_enviar})
    elif 'email' in datos and 'contraseña' in datos:
        email = datos['email']
        contraseña = datos['contraseña']
        usuario = Usuario.buscar(email=email)
    if len(usuario) > 1:
        return JsonResponse({'Mensaje': 'Error: Múltiples usuarios registrados al mismo correo.'})
    elif len(usuario) < 1:
        return JsonResponse({'Mensaje': 'Error: Ningún usuario encontrado con el email proporcionado.'})
    else:
        usuario = usuario[0]
        if usuario.autenticar(contraseña):
            dict_a_enviar = usuario.__dict__
            dict_a_enviar.pop('contraseña')
            dict_a_enviar['_id'] = str(dict_a_enviar['_id'])
            return JsonResponse({'Usuario': dict_a_enviar, 'token_sesion': usuario.crear_sesion()})

def buscar_objetos(request):
    encontrados = ObjetoDeAprendizaje.buscar(request.GET['cadena_de_busqueda'])
    encontrados_serializables = [encontrado.serializar_para_tabla() for encontrado in encontrados]
    return JsonResponse({'objetos_encontrados': encontrados_serializables})

def registrar_objeto(request):
    datos_objeto = json.loads(request.body)
    objeto = ObjetoDeAprendizaje(
        nombre=datos_objeto["nombre_objeto"],
        nivel=datos_objeto["nivel_objeto"],
        granularidad=datos_objeto["granularidad_objeto"],
        perfil=datos_objeto["perfil_objeto"],
        objetivo_de_aprendizaje=datos_objeto["objetivo_objeto"],
        temas=[tema.lower() for tema in datos_objeto["temas"]],
        materiales=datos_objeto["materiales"],
        descripcion=datos_objeto["desc_objeto"]
    )
    objeto.guardar()
    return JsonResponse({'Mensaje': "Exito"})

def arreglar_csrf(request):
    plantilla=loader.get_template("manejador/arreglar_csrf.html")
    if request.method == "POST" :
        return HttpResponse(plantilla.render({}, request))
    return HttpResponse(plantilla.render({}, request))