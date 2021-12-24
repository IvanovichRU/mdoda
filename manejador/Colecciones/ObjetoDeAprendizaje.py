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
    id: str
    nombre: str
    descripcion: str
    nivel: str
    granularidad: int
    perfil: str
    objetivo_de_aprendizaje: str
    temas: 'list[Tema]'
    autor: Usuario
    materiales: 'list[Material]'

    def __init__(
        self, nombre=None, nivel=None,
        granularidad=None, perfil=None,
        objetivo_de_aprendizaje=None,
        temas=None, autor=None, materiales=None, dict_mongo=None) -> None:

        if (dict_mongo):
            self.id = dict_mongo['_id']
            self.nombre = dict_mongo['NombreDelObjeto']
            self.nivel = dict_mongo['Nivel']
            self.granularidad = dict_mongo['Granularidad']
            self.perfil = dict_mongo['Perfil']
            self.objetivo_de_aprendizaje = dict_mongo['ObjetivoDeAprendizaje']
            self.temas = dict_mongo['Temas']
            self.autor = Usuario(mongo_id=dict_mongo['Autor']['id'], mongo_tipo=dict_mongo['Autor']['tipo'])
            self.materiales = dict_mongo['Materiales']
            self.descripcion = dict_mongo['Descripcion']
        else:
            self.nombre = nombre
            self.nivel = nivel
            self.granularidad = granularidad
            self.perfil = perfil
            self.objetivo_de_aprendizaje = objetivo_de_aprendizaje
            self.temas = temas
            self.autor = autor
            self.materiales = materiales

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
            'id': str(self.id),
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'temas': self.temas
        }
        return objeto