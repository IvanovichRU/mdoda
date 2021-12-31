from bson.objectid import ObjectId
from mdoda.conexion_mongo import mongoDB
from cryptography.fernet import Fernet

fernet = Fernet(b'InIsfWfmkVIZZT5NNZy4f2zmAPiilrQzngNbotO92S4=')

class Usuario:
    _id: str
    nombre: str
    apellidos: str
    email: str
    tipo: str
    contraseña: str

    def __str__(self) -> str:
        return self.nombre + ' ' + self.apellidos
    
    def __init__(self, dict_mongo: dict=None, **kwargs):
        '''
        Un objeto `Usuario` acepta un diccionario extraido desde mongoDB o
        creado manualmente, con los atributos: `nombre`, `apellidos`, `email`,
        `tipo` y `contraseña`. Se pueden modificar posteriormente mediante `kwargs`.
        '''
        if 'id_mongo' in kwargs and 'tipo' in kwargs:
            if kwargs['tipo'] == 'Administrador':
                self.__dict__ = mongoDB.Administradores.find_one({'_id':ObjectId(kwargs['id_mongo'])})
                self.tipo = 'Administrador'
            elif kwargs['tipo'] == 'Maestro':
                self.__dict__ = mongoDB.Maestros.find_one({'_id':ObjectId(kwargs['id_mongo'])})
                self.tipo = 'Maestro'
            self.objetos = len([objeto for objeto in mongoDB.ObjetosDeAprendizaje.find({'autor':self._id})])
        else:
            self._id = dict_mongo['_id'] if '_id' in dict_mongo else None
            self.nombre = dict_mongo['nombre']
            self.apellidos = dict_mongo['apellidos']
            self.email= dict_mongo['email']
            self.tipo = dict_mongo['tipo']
            self.contraseña = dict_mongo['contraseña']
            self.objetos = len([objeto for objeto in mongoDB.ObjetosDeAprendizaje.find({'autor':self._id})])

    def guardar(self):
        if self.tipo == 'Administrador':
            dict_para_mongo = self.__dict__
            dict_para_mongo.pop('tipo')
            dict_para_mongo['contraseña'] = fernet.encrypt(dict_para_mongo['contraseña'].encode())
            if dict_para_mongo['_id'] is None:
                dict_para_mongo.pop('_id')
            mongoDB.Administradores.insert_one(dict_para_mongo)
        elif self.tipo == 'Maestro':
            dict_para_mongo = self.__dict__
            dict_para_mongo.pop('tipo')
            dict_para_mongo['contraseña'] = fernet.encrypt(dict_para_mongo['contraseña'].encode())
            mongoDB.Maestros.insert_one(self.__dict__)
        else:
            mongoDB.Alumnos.insert_one(self.__dict__)

    def autenticar(self, contraseña: str) -> bool:
        if contraseña == self.contraseña:
            return True
        else:
            return False

    def crear_sesion(self) -> ObjectId:
        return mongoDB.Sesiones.insert_one({'usuario': self._id, 'tipo': self.tipo}).inserted_id

    @staticmethod
    def buscar(**kwargs) -> 'list[Usuario] | Usuario | None':
        '''Para buscar un usuario es necesario proveer algún atributo 
        o conjunto de ellos, de la clase `Usuario`.'''
        dict_a_buscar = {}
        usuarios_encontrados = []
        for key in kwargs:
            if key in ['_id', 'nombre', 'email', 'apellidos', 'contraseña']:
                dict_a_buscar[key] = kwargs[key]
        for usuario in mongoDB.Administradores.find(dict_a_buscar):
            usuario['tipo'] = 'Administrador'
            usuario['contraseña'] = fernet.decrypt(usuario['contraseña']).decode()
            usuarios_encontrados.append(Usuario(usuario))
        for usuario in mongoDB.Maestros.find(dict_a_buscar):
            usuario['tipo'] = 'Maestro'
            usuario['contraseña'] = fernet.decrypt(usuario['contraseña']).decode()
            usuarios_encontrados.append(Usuario(usuario))
        for usuario in mongoDB.Alumnos.find(dict_a_buscar):
            usuario['tipo'] = 'Alumno'
            usuarios_encontrados.append(usuario)
        return usuarios_encontrados

    @staticmethod
    def obtener(_id: ObjectId) -> 'Usuario':
        '''Regresa un `Usuario` correspondiente al _id proporcionado.'''
        usuario = mongoDB.Administradores.find_one({'_id': _id})
        if usuario is not None:
            usuario['contraseña'] = fernet.decrypt(usuario['contraseña']).decode()
            usuario['tipo'] = 'Administrador'
            return Usuario(usuario)
        usuario = mongoDB.Maestros.find_one({'_id': _id})
        if usuario is not None:
            usuario['contraseña'] = fernet.decrypt(usuario['contraseña']).decode()
            usuario['tipo'] = 'Maestro'
            return Usuario(usuario)
        usuario = mongoDB.Alumnos.find_one({'_id': _id})
        usuario['tipo'] = 'Alumno'
        if usuario is not None:
            return Usuario(usuario)
        else:
            return None

    @staticmethod
    def recuperar_sesion(token: str) -> 'Usuario':
        sesion = mongoDB.Sesiones.find_one({'_id': ObjectId(token)})
        if sesion is not None:
            if sesion['tipo'] == 'Administrador':
                dict_usuario = mongoDB.Administradores.find_one({'_id': ObjectId(sesion['usuario'])})
                dict_usuario['tipo'] = 'Administrador'
                return Usuario(dict_usuario)
            else:
                dict_usuario = mongoDB.Maestros.find_one({'_id': ObjectId(sesion['usuario'])})
                dict_usuario['tipo'] = 'Maestro'
                return Usuario(dict_usuario)
        else:
            return None
