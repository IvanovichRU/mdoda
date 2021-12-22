from mdoda.conexion_mongo import mongoDB
from cryptography.fernet import Fernet

fernet = Fernet(b'InIsfWfmkVIZZT5NNZy4f2zmAPiilrQzngNbotO92S4=')

class Usuario:
    nombre: str
    apellidos: str
    email: str
    tipo: str
    contraseña: str

    def __str__(self) -> str:
        return self.nombre + ' ' + self.apellidos
    
    def __init__(self, nombre: str, apellidos: str, email: str, contraseña: str, tipo: str, usuario_id) -> None:
        self.nombre = nombre
        self. apellidos = apellidos
        self.email = email
        self.contraseña = contraseña
        self.tipo = tipo
        self.usuario_id = usuario_id

    @staticmethod
    def guardar(usuario: dict):
        contraseña = usuario['contraseña']
        contraseña = fernet.encrypt(contraseña.encode())
        if usuario['tipo'] == 'administrador':
            mongoDB.Administradores.insert_one({
                'nombre': usuario['nombre'] if 'nombre' in usuario else '',
                'apellidos': usuario['apellidos'] if 'apellidos' in usuario else '',
                'email': usuario['email'],
                'contraseña': contraseña
            })
        elif usuario.tipo == 'maestro':
            mongoDB.Maestros.insert_one({
                'nombre': usuario['nombre'] if 'nombre' in usuario else '',
                'apellidos': usuario['apellidos'] if 'apellidos' in usuario else '',
                'email': usuario['email'],
                'contraseña': contraseña
            })
        else:
            mongoDB.Alumnos.insert_one({
                'nombre': usuario['nombre'] if 'nombre' in usuario else '',
                'apellidos': usuario['apellidos'] if 'apellidos' in usuario else '',
                'email': usuario['email'],
                'contraseña': contraseña
            })

    @staticmethod
    def buscar(email: str, contraseña: str):
        usuario_encontrado = mongoDB.Administradores.find_one({'email': email})
        if usuario_encontrado:
            contraseña_real = fernet.decrypt(mongoDB.Administradores.find_one({'_id': usuario_encontrado['_id']})['contraseña']).decode()
            if contraseña == contraseña_real:
                return Usuario(usuario_encontrado['nombre'], usuario_encontrado['apellidos'], usuario_encontrado['email'], usuario_encontrado['contraseña'], 'administrador', usuario_encontrado['_id'])
            else:
                return None
        usuario_encontrado = mongoDB.Maestros.find_one({'email': email})
        if usuario_encontrado:
            return Usuario(usuario_encontrado['nombre'], usuario_encontrado['apellidos'], usuario_encontrado['email'], usuario_encontrado['contraseña'], 'maestro')
        usuario_encontrado = mongoDB.Alumnos.find_one({'email': email})
        if usuario_encontrado:
            return Usuario(usuario_encontrado['nombre'], usuario_encontrado['apellidos'], usuario_encontrado['email'], usuario_encontrado['contraseña'], 'alumno')

    @staticmethod
    def obtener(id: str):
        usuario_encontrado = mongoDB.Administradores.find_one({'_id': id})
        if usuario_encontrado:
            return Usuario(usuario_encontrado['nombre'], usuario_encontrado['apellidos'], usuario_encontrado['email'], usuario_encontrado['contraseña'], 'administrador', usuario_encontrado['_id'])
        usuario_encontrado = mongoDB.Maestros.find_one({'_id': id})
        if usuario_encontrado:
            return Usuario(usuario_encontrado['nombre'], usuario_encontrado['apellidos'], usuario_encontrado['email'], usuario_encontrado['contraseña'], 'maestro', usuario_encontrado['_id'])
        usuario_encontrado = mongoDB.Alumnos.find_one({'_id': id})
        if usuario_encontrado:
            return Usuario(usuario_encontrado['nombre'], usuario_encontrado['apellidos'], usuario_encontrado['email'], usuario_encontrado['contraseña'], 'alumno', usuario_encontrado['_id'])
        return None

    @staticmethod
    def todos():
        return [Usuario(usuario['nombre'], usuario['apellidos'], usuario['email'], fernet.decrypt(usuario['contraseña']).decode(), 'administrador') for usuario in mongoDB.Administradores.find()]
