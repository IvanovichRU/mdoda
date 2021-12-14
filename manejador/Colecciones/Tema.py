from mdoda.conexion_mongo import mongoDB

class Tema:
    tema: str

    def __init__(self, tema: str) -> None:
        self.tema = tema

    def __str__(self) -> str:
        return self.tema

    def guardar(self):
        mongoDB.Temas.insert_one(self.__dict__)

    @staticmethod
    def todos():
        return [Tema(tema['tema']) for tema in mongoDB.Temas.find()]

    @staticmethod
    def buscar(tema: str):
        return [Tema(tema['tema']) for tema in mongoDB.Temas.find({'tema': tema})]