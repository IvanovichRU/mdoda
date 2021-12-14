from django.http import HttpResponse

from mdoda.conexion_mongo import db
import datetime

# Create your views here.
def index(request):
    documento = {'hora': datetime.datetime.now()}
    db.Materiales.insert_one(documento)
    return HttpResponse("Hola, Aldha!");