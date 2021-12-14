from mdoda.conexion_mongo import mongoDB

class Material:
    fuente : str
    tipo_de_material: str

    def __init__(self, fuente: str = None, tipo_material: str = None):
        self.fuente = fuente
        self.tipo_de_material = tipo_material

    def __str__(self) -> str:
        return self.fuente + self.tipo_de_material

    def cambiar_fuente(self, fuente: str):
        self.fuente = fuente

    def cambiar_tipo_de_material(self, tipo_material: str):
        self.tipo_de_material= tipo_material

    # @staticmethod
    # def todos():
    #     return [Material(material.).__str__() for material in mongoDB.Materiales.find()]

    # Tipo de material: extensión del material.
    # Fuente: Nombre del material.