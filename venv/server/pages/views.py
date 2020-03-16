from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
import pyrebase
import json
import requests
import geocoder

url = 'https://maps.googleapis.com/maps/api/geocode/json'
# apikey='AIzaSyByksrWBWJYbWJenGuIhUZXVceTh5sNjqI'

config = {
    'apiKey': "AIzaSyCOjXOsWfXTVrUlvbNorZdTyJO3yOCinlI",
    'authDomain': "prediction-b4653.firebaseapp.com",
    'databaseURL': "https://prediction-b4653.firebaseio.com",
    'projectId': "prediction-b4653",
    'storageBucket': "prediction-b4653.appspot.com",
    'messagingSenderId': "106176267749",
}

firebase = pyrebase.initialize_app(config)
authe=firebase.auth()
db = firebase.database()

# Create your views here.
def map(request, *args, **kwargs):
    return render(request, "map.html", {})

def login(request, *args, **kwargs):
    return render(request, "login.html", {})

def regi(request, *args, **kwargs):
    return render(request, "regi.html")

def profile(request, *args, **kwargs):
    return render(request, "profile.html")

def postsign(request):
        eml = request.POST.get('email')
        passw = request.POST.get('password')
        try:
                user = authe.sign_in_with_email_and_password(eml,passw)
        except:
                message = "invalid credentials"
                return render(request, "login.html", {"msg":message})
        print(user)
        print(user['idToken'])
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        return render(request, "afterlogin.html")


def postsignup(request):
         hname = request.POST.get('Hospital name')
         heml = request.POST.get('Email')
         husername = request.POST.get('Username')
         hpassw = request.POST.get('Password')
         hcpassw = request.POST.get('Confirm Password')
         hcountry = request.POST.get('Country')
         hstate = request.POST.get('State')
         hadd = request.POST.get('Address')
         hpincode = request.POST.get('Pin code')
         hphno = request.POST.get('Contact no')

         # params = {'sensor': 'false', 'address': 'Mountain View, CA'}
         # r = requests.get(url, params=params)
         # results = r.json()['results']
         # location = results[0]['geometry']['location']
         # location['lat'], location['lng']

         # g = geocoder.google('Mountain View, CA')
         # g.latlng



         try:
               user = authe.create_user_with_email_and_password(heml, hpassw)
               uid = user['localId']
               data = {"h_name": hname, "h_email": heml, "h_username": husername, "h_passw": hpassw,
                       "h_country": hcountry, "h_state": hstate, "h_add": hadd, "h_pincode": hpincode, "h_phno": hphno}
               db.child("users").child(uid).child("details").set(data)

         except:
            message = "Unable to create account try again"
            return render(request, "regi.html", {"messg": message})

         return render(request, "login.html")

def postaftersign(request):
    hdis = request.POST.get('Dis')
    hvacc = request.POST.get('Vac')
    hprev=request.POST.get('preventions')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    data1 = {"disease": hdis,"preventions":hprev,"vaccines": hvacc}
    db.child("users").child(a).child("info").set(data1)
    return render(request, "afterlogin.html")

def postprofile(request):
    print("*******")
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    Hospital= db.child("users").child(a).child("details").child('h_name').get().val()
    print(Hospital)
    email =db.child("users").child(uid).child("details").child('h_email').get().val()
    address=db.child("users").child(uid).child("details").child('h_add').get().val()
    phno=db.child("users").child(uid).child("details").child('h_phno'). get().val()
    dis=db.child("users").child(a).child("info").child('disease').get().val()
    vacc=db.child("users").child(a).child("info"). child('vaccine').get().val()
    return render(request, "profile.html",{'Hn':Hospital,'eml':email,'add':address,'phn':phno,'d':dis,'vac':vacc})