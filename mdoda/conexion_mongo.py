from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
mongoDB = client.BaseDeConocimiento

PREPOSICIONES = [
    'a',
    'ante',
    'bajo',
    'cabe',
    'con',
    'contra',
    'de',
    'desde',
    'durante',
    'en',
    'entre',
    'hacia',
    'hasta',
    'mediante',
    'para',
    'por',
    'según',
    'sin',
    'so',
    'sobre',
    'tras',
    'versus',
    'vs'
]

ARTICULOS = [
    'el',
    'la',
    'los',
    'las',
    'un',
    'una',
    'unos',
    'unas'
]
