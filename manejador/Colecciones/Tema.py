from bson.objectid import ObjectId
from mdoda.conexion_mongo import mongoDB

class Tema:
    _id: ObjectId
    tema: str
    objetos: 'list[ObjectId]'

    def __init__(self, tema: str=None, objetos: 'list[ObjectId]'=[], **kwargs) -> None:
        if 'id_mongo' in kwargs:
            dict_tema = mongoDB.Temas.find_one({'_id': kwargs['id_mongo']})
            if dict_tema:
                self._id = dict_tema['_id']
                self.tema = dict_tema['tema']
                self.objetos = dict_tema['objetos']
        else:
            self._id = None
            self.tema = tema
            self.objetos = objetos

    def __str__(self) -> str:
        return self.tema

    def guardar(self):
        dict_para_mongo = self.__dict__
        dict_para_mongo.pop('_id')
        self._id = mongoDB.Temas.insert_one(dict_para_mongo).inserted_id

    def actualizar(self):
        if self._id:
            dict_para_mongo = self.__dict__
            mongoDB.Temas.replace_one({'_id': self._id}, {"tema":dict_para_mongo["tema"], "objetos":dict_para_mongo["objetos"]})

    def agregar_id_objeto(self, id_objeto: ObjectId):
        self.objetos.append(id_objeto)

    def agregar_ids_objetos(self, ids_objetos: 'list[ObjectId]'):
        [self.objetos.append(objeto) for objeto in ids_objetos]

    @staticmethod
    def obtener(mongo_id):
        tema_encontrado = mongoDB.Temas.find_one({'_id': mongo_id})
        if tema_encontrado:
            return tema_encontrado
        else:
            return None

    @staticmethod
    def todos():
        return [Tema(tema['tema']) for tema in mongoDB.Temas.find()]

    @staticmethod
    def buscar(tema: str):
        return [Tema(tema['tema']) for tema in mongoDB.Temas.find({'tema': tema})]
