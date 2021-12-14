from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
mongoDB = client.BaseDeConocimiento
