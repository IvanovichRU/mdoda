import json
from bson.objectid import ObjectId
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
            if datos['recordar'] == True:
                token_sesion = str(usuario.crear_sesion())
            else:
                token_sesion = None
            respuesta = JsonResponse({'Usuario': dict_a_enviar, 'token_sesion': token_sesion})
            return respuesta

def buscar_objetos(request):
    encontrados = ObjetoDeAprendizaje.buscar(request.GET['cadena_de_busqueda'])
    encontrados_serializables = [encontrado.serializar_para_tabla() for encontrado in encontrados]
    return JsonResponse({'objetos_encontrados': encontrados_serializables})

def registrar_objeto(request):
    datos = json.loads(request.body)
    datos['autor'] = ObjectId(datos['autor'])
    objeto = ObjetoDeAprendizaje(dict_mongo=datos)
    objeto.guardar()
    return JsonResponse({'Mensaje': "Exito"})

def arreglar_csrf(request):
    plantilla=loader.get_template("manejador/arreglar_csrf.html")
    if request.method == "POST" :
        return HttpResponse(plantilla.render({}, request))
    return HttpResponse(plantilla.render({}, request))

def obtener_objetos(request):
    datos = request.GET
    objetos_del_usuario = ObjetoDeAprendizaje.buscar_objetos_de_usuario(datos['usuario_id'], serializar=True)
    return JsonResponse({'objetos_encontrados': objetos_del_usuario})

def refrescar_usuario(request):
    datos = request.GET
    dict_a_enviar = Usuario(id_mongo=datos['usuario_id'], tipo=datos['tipo']).__dict__
    dict_a_enviar['_id'] = str(dict_a_enviar['_id'])
    dict_a_enviar.pop('contraseña')
    return JsonResponse({'usuario_actualizado':dict_a_enviar})