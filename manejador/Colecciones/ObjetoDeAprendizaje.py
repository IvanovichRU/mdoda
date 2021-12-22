from mdoda.conexion_mongo import mongoDB
from mdoda.conexion_mongo import PREPOSICIONES, ARTICULOS

from .Tema import Tema
from .Usuario import Usuario
from .Material import Material

from enum import Enum

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
    nombre: str
    nivel: str
    granularidad: int
    perfil: str
    objetivo_de_aprendizaje: str
    temas: 'list[Tema]'
    autor: Usuario
    materiales: 'list[Material]'

    def __init__(
        self, nombre, nivel,
        granularidad, perfil,
        objetivo_de_aprendizaje,
        temas, autor, materiales) -> None:

        self.nombre = nombre
        self.nivel = nivel
        self.granularidad = granularidad
        self.perfil = perfil
        self.objetivo_de_aprendizaje = objetivo_de_aprendizaje
        self.temas = temas
        self.autor = autor
        self.materiales = materiales

    @staticmethod
    def buscar(cadena_búsqueda: str):
        for preposicion in PREPOSICIONES:
            cadena_búsqueda = cadena_búsqueda.replace(' ' + preposicion + ' ', ', ')
            cadena_búsqueda = cadena_búsqueda.replace(' ' + preposicion, ', ')
            cadena_búsqueda = cadena_búsqueda.replace(preposicion + ' ', ', ')
        for articulo in ARTICULOS:
            cadena_búsqueda = cadena_búsqueda.replace(' ' + articulo + ' ', ', ')
            cadena_búsqueda = cadena_búsqueda.replace(' ' + articulo, ', ')
            cadena_búsqueda = cadena_búsqueda.replace(articulo + ' ', ', ')
        cadena_búsqueda = cadena_búsqueda.split(', ')
        return cadena_búsqueda
