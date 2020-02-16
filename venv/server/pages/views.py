from django.shortcuts import render
from django.http import HttpResponse
import pyrebase
import json

config = {
'apiKey': "AIzaSyCOjXOsWfXTVrUlvbNorZdTyJO3yOCinlI",
'authDomain': "prediction-b4653.firebaseapp.com",
'databaseURL': "https://prediction-b4653.firebaseio.com",
'projectId': "prediction-b4653",
'storageBucket': "prediction-b4653.appspot.com",
'messagingSenderId': "106176267749 "
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
# Create your views here.
def map(request, *args, **kwargs):
        data = database.child("diseases").get()
        diseases = json.dumps(data.val())
        print(diseases)
        return render(request,"map.html",{"data": diseases})

def login(request, *args, **kwargs):
        return render(request,"login.html",{})