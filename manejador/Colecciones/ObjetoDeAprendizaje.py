from mdoda.conexion_mongo import mongoDB
from mdoda.conexion_mongo import PREPOSICIONES, ARTICULOS

from .Tema import Tema
from .Usuario import Usuario
from .Material import Material

from enum import Enum
from difflib import SequenceMatcher

class Nivel(Enum):
    PREPARATORIA = 1
    LICENCIATURA = 2
    MAESTRÍA     = 3
    DOCTORADO    = 4

class Granularidad(Enum):
    CARRERA = 1
    MATERIA = 2
    TEMA    = 3
    SUBTEMA = 4

class ObjetoDeAprendizaje:
    _id: str
    nombre: str
    descripcion: str
    nivel: str
    granularidad: int
    perfil: str
    objetivo_de_aprendizaje: str
    temas: 'list[str]'
    autor: Usuario
    materiales: 'list[Material]'

    def __init__(
        self, nombre=None, nivel=None,
        granularidad=None, perfil=None,
        objetivo_de_aprendizaje=None, descripcion=None,
        temas=None, autor=None, materiales=None, **kwargs) -> None:

        if 'dict_mongo' in kwargs:
            self.__dict__ = kwargs['dict_mongo']
        else:
            self._id = None
            self.nombre = nombre
            self.nivel = nivel
            self.granularidad = granularidad
            self.perfil = perfil
            self.objetivo_de_aprendizaje = objetivo_de_aprendizaje
            self.temas = temas
            self.autor = autor
            self.materiales = materiales
            self.descripcion = descripcion
    
    def guardar(self):
        dict_para_mongo = self.__dict__
        self._id = mongoDB.ObjetosDeAprendizaje.insert_one(dict_para_mongo).inserted_id
        for tema_actual in self.temas:
            encontrado = mongoDB.Temas.find_one({'tema': tema_actual})
            print(encontrado)
            if encontrado is None:
                nuevo_tema = Tema(tema_actual, [])
                nuevo_tema.agregar_id_objeto(self._id)
                print(nuevo_tema.objetos)
                nuevo_tema.guardar()
            else:
                tema_existente = Tema(id_mongo=encontrado['_id'])
                print(tema_existente.__dict__)
                if str(self._id) not in [str(id_objeto) for id_objeto in tema_existente.objetos]:
                    tema_existente.agregar_id_objeto(self._id)
                    tema_existente.actualizar()

    def actualizar(self, dict_cambios: dict):
        dict_nuevo = mongoDB.ObjetosDeAprendizaje.replace_one({'_id': self._id}, dict_cambios)
        self.__dict__ = dict_nuevo

    @staticmethod
    def buscar(cadena_busqueda: str):
        cadenas_a_buscar = []
        cadenas_a_buscar.append(cadena_busqueda)
        [cadenas_a_buscar.append(cadena) for cadena in cadena_busqueda.split(' ')]
        set_cadenas_a_buscar = set(cadenas_a_buscar) - set(PREPOSICIONES) - set(ARTICULOS)
        lista_final_temas_busqueda = list(set_cadenas_a_buscar)
        lista_final_temas_busqueda.sort(key=lambda s: len(s), reverse=True)
        temas = [tema for tema in mongoDB.Temas.find()]
        objetos_encontrados = []
        for cuenta, tema_busqueda in enumerate(lista_final_temas_busqueda):
            if cuenta > 3:
                break
            for tema in temas:
                tema_cadena = tema['tema']
                similitud = SequenceMatcher(None, tema_cadena.lower(), tema_busqueda.lower()).ratio()
                if similitud >= 0.75:
                    if 'objetos' in tema:
                        for objeto in tema['objetos']:
                            if objeto not in [objeto for objeto in objetos_encontrados]:
                                objetos_encontrados.append(objeto)
        lista_objetos_finales = []
        for objeto_id in objetos_encontrados:
            lista_objetos_finales.append(ObjetoDeAprendizaje(dict_mongo=mongoDB.ObjetosDeAprendizaje.find_one({'_id': objeto_id})))
        return lista_objetos_finales

    def serializar_para_tabla(self):
        objeto = {
            'id': str(self._id),
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'temas': self.temas
        }
        return objeto
