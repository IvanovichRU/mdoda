import json
from django.http.response import HttpResponse, JsonResponse
from manejador.Colecciones.Usuario import Usuario
from manejador.Colecciones.ObjetoDeAprendizaje import ObjetoDeAprendizaje
from django.template import loader
from django.core.files.storage import FileSystemStorage
from mdoda.settings import BASE_DIR

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
        else:
            return JsonResponse({'Mensaje': 'Contraseña incorrecta.'})

def buscar_objetos(request):
    encontrados = ObjetoDeAprendizaje.buscar(request.GET['cadena_de_busqueda'])
    encontrados_serializables = [encontrado.serializar_para_tabla() for encontrado in encontrados]
    return JsonResponse({'objetos_encontrados': encontrados_serializables})

def registrar_objeto(request):
    archivo_zip = request.FILES['zip']
    almacenamiento = FileSystemStorage(location=BASE_DIR / 'objetos/')
    archivo = almacenamiento.save(archivo_zip.name, archivo_zip)
    datos = json.loads(request.POST['datos'])
    datos['url'] = almacenamiento.path(archivo)
    ObjetoDeAprendizaje(dict_mongo=datos).guardar()
    return JsonResponse({'Mensaje': "Exito"})

def nuevo_usuario(request):
    datos = json.loads(request.body)
    usuario_nuevo = Usuario(datos)
    usuario_nuevo.guardar()
    return JsonResponse({'Mensaje': 'Nuevo usuario creado.'})

def arreglar_csrf(request):
    plantilla=loader.get_template("manejador/arreglar_csrf.html")
    if request.method == "POST" :
        return HttpResponse(plantilla.render({}, request))
    return HttpResponse(plantilla.render({}, request))

def obtener_objetos(request):
    datos = request.GET
    objetos = Usuario(id_mongo=datos['usuario_id'], tipo=datos['tipo']).obtener_objetos()
    return JsonResponse({'objetos_encontrados': objetos})

def obtener_info_objeto(request):
    datos = request.GET
    objeto = ObjetoDeAprendizaje(id_mongo=datos['_id'])
    return JsonResponse({'Objeto': objeto.serializar_info()})

def descargar_objeto(request):
    datos = request.GET
    url_objeto = ObjetoDeAprendizaje(id_mongo=datos['_id']).url
    # return JsonResponse({'Mensaje': 'Exito'})
    try:
        with open(url_objeto, 'rb') as f:
            archivo_zip = f.read()
            return HttpResponse(archivo_zip, headers={
                'Content-Type': 'application/zip',
                'Content-Disposition': 'attachment; filename="Objeto.zip"'
            })
    except IOError:
        return JsonResponse({'Mensaje': 'Error'})

def refrescar_usuario(request):
    datos = request.GET
    dict_a_enviar = Usuario(id_mongo=datos['usuario_id'], tipo=datos['tipo']).__dict__
    dict_a_enviar['_id'] = str(dict_a_enviar['_id'])
    dict_a_enviar.pop('contraseña')
    return JsonResponse({'usuario_actualizado':dict_a_enviar})