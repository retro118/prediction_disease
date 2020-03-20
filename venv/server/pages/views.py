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
    data = db.child("diseases").get()
    diseases = json.dumps(data.val())
    print(diseases)
    return render(request, "map.html", {"data": diseases})

def login(request, *args, **kwargs):
    return render(request, "login.html", {})

def regi(request, *args, **kwargs):
    return render(request, "regi.html")



# DISPLAY
def profile(request, *args, **kwargs):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    # def listToString(s):
    #      str1 = " "
    #      return (str1.join(s))

    # const1=db.child("h").shallow().get().val()
    # print (">>>>",const1)
    # c1= listToString(const1)
    # print ("******", c1)

    Hospital =db.child("users1").child(a).child("user").child('h_name').get().val()
    email =  db.child("users1").child(a).child("user").child('h_email').get().val()
    address = db.child("users1").child(a).child("user").child('h_address').get().val()
    phno = db.child("users1").child(a).child("user").child('phone').get().val()
    # dis = c4
    # vacc =db.child("users").child(a).child("disease").child(c4).child('vaccine').child('v1').get().val()
    # return render(request, "profile.html",
    #                {'Hn': Hospital, 'eml': email, 'add': address, 'phn': phno, 'd': dis, 'vac': vacc})
    return render(request, "profile.html",
                  {'Hn': Hospital, 'eml': email, 'add': address, 'phn': phno})



# LOGIN
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


# REGISTRATION
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


               address={"address":hadd,"Email":heml,"Phone":hphno,"Country":hcountry,"State":hstate}
               lat={"lat":'27',"lng":'28'}
               v={"v1":'aaa'}
               data={"h_name":hname,"phone":hphno,"pincode":hpincode,"username":husername,"password":hpassw ,"h_email": heml,"h_address":hadd}

               # hospital database
               db.child("h").child(hname).set(address)
               db.child("h").child(hname).child("location").set(lat)
               db.child("h").child(hname).child("vaccine").child("vacc").set(v)

                 # user database
               db.child("users1").child(uid).child("user").set(data)


         except:
            message = "Unable to create account try again"
            return render(request, "regi.html", {"messg": message})

         return render(request, "login.html")


# AFTER LOGIN ADD INFO ABOUT DISEASE AND VACCINE
def postaftersign(request):

    harc=request.POST.get('acr')
    hspc=request.POST.get('special')
    hfac=request.POST.get('fac')
    hdis = request.POST.get('Dis')
    hvacc = request.POST.get('Vac')
    hprev=request.POST.get('preventions')
    hsymp=request.POST.get('symp')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    p={"p1":hprev}
    s={"s1":hsymp}
    lat = {"lat": '27', "lng": '28'}


    db.child("disease1").child(hdis).set(lat)
    db.child("disease1").child(hdis).child("precautions").set(p)
    db.child("disease1").child(hdis).child("symptoms").set(s)


    d={"Accredation":harc,"Speciality":hspc,"Facility":hfac}
    db.child("users1").child(a).child("user").child("a_info").set(d)

    return render(request, "afterlogin.html")
