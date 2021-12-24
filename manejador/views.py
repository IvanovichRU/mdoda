import json
from django.http.response import JsonResponse
from manejador.Colecciones.Usuario import Usuario
from manejador.Colecciones.ObjetoDeAprendizaje import ObjetoDeAprendizaje

# Create your views here.
def vista_login(request):
    datos = json.loads(request.body)
    email = datos['email']
    contraseña = datos['contraseña']
    usuario = Usuario.buscar(email, contraseña)
    return JsonResponse({
        'nombre': usuario.nombre,
        'apellidos': usuario.apellidos,
        'email': usuario.email,
        'tipo': usuario.tipo,
        'id': str(usuario.usuario_id)
    })

def buscar_objetos(request):
    encontrados = ObjetoDeAprendizaje.buscar(request.GET['cadena_de_busqueda'])
    encontrados_serializables = [encontrado.serializar_para_tabla() for encontrado in encontrados]
    return JsonResponse({'objetos_encontrados': encontrados_serializables})
