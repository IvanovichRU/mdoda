import json
from django.http.response import JsonResponse
from manejador.Colecciones.Usuario import Usuario

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
    datos = json.loads(request.body)
    return None
