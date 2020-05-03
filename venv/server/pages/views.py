from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
import pyrebase
import json
import requests
import geocoder

# url = 'https://maps.googleapis.com/maps/api/geocode/json'
# api_key = 'AIzaSyByksrWBWJYbWJenGuIhUZXVceTh5sNjqI'

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
    data_h = db.child("hospitals").get()
    diseases = json.dumps(data.val())
    h = json.dumps(data_h.val())
    print(diseases)
    print(">>>>",h)

    return render(request, "map.html", {"data": diseases,"data_h":h})


def login(request, *args, **kwargs):
    return render(request, "login.html")

def regi(request, *args, **kwargs):
    return render(request, "regi.html")

def addprofile(request, *args, **kwargs):
    return render(request, "addprofile.html")




# LOGIN
def postsign(request):
        eml = request.POST.get('email')
        passw = request.POST.get('password')

        try:
                user = authe.sign_in_with_email_and_password(eml,passw)

        except:
                message = "The Email or Password you entered is incorrect. "
                return render(request, "login.html", {"msg":message})
        print(user)
        print(user['idToken'])
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        idtoken = request.session['uid']
        a = authe.get_account_info(idtoken)
        a = a['users']
        a = a[0]
        a = a['localId']

        Hospital = db.child("users1").child(a).child("user").child('h_name').get().val()
        email = db.child("users1").child(a).child("user").child('h_email').get().val()
        address = db.child("users1").child(a).child("user").child('h_address').get().val()
        phno = db.child("users1").child(a).child("user").child('phone').get().val()
        vacc = db.child("hospitals").child(Hospital).child('vaccine').get().val()
        mylist=", ".join(vacc)
        return render(request, "profile.html",
                      {'Hn': Hospital, 'eml': email, 'add': address, 'phn': phno, 'vac': mylist})




# DISPLAY PROFILE
def profile(request, *args, **kwargs):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    Hospital =db.child("users1").child(a).child("user").child('h_name').get().val()
    print (Hospital)
    email =  db.child("users1").child(a).child("user").child('h_email').get().val()
    print (email)
    address = db.child("users1").child(a).child("user").child('h_address').get().val()
    print (address)
    phno = db.child("users1").child(a).child("user").child('phone').get().val()
    vacc=db.child("hospitals").child(Hospital).child('vaccine').get().val()
    mylist = ", ".join(vacc)

    return render(request, "addprofile.html",
                   {'Hn': Hospital, 'eml': email, 'add': address, 'phn': phno,'vac':mylist})


# ADD VACCINES
def profilepost(request, *args, **kwargs):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print ("************",a)


    vname = request.POST.get('fname')
    hname = db.child("users1").child(a).child("user").child('h_name').get().val()
    result=db.child("hospitals").child(hname).child("vaccine").get().val()
    print(len(result))
    result.append(vname)
    v=db.child("hospitals").child(hname).child("vaccine").set(result)


    Hospital = db.child("users1").child(a).child("user").child('h_name').get().val()

    email = db.child("users1").child(a).child("user").child('h_email').get().val()

    address = db.child("users1").child(a).child("user").child('h_address').get().val()

    phno = db.child("users1").child(a).child("user").child('phone').get().val()
    vacc = db.child("hospitals").child(Hospital).child('vaccine').get().val()
    mylist = ",".join(vacc)

    return render(request, "addprofile.html",{'Hn': Hospital, 'eml': email, 'add': address, 'phn': phno,'vac':mylist})

# DELETE VACCINES
def profilepostdel(request, *args, **kwargs):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    hname = db.child("users1").child(a).child("user").child('h_name').get().val()
    result = db.child("hospitals").child(hname).child("vaccine").get().val()
    print("==========",result)
    del result[-1]
    v=db.child("hospitals").child(hname).child("vaccine").set(result)
    Hospital = db.child("users1").child(a).child("user").child('h_name').get().val()

    email = db.child("users1").child(a).child("user").child('h_email').get().val()

    address = db.child("users1").child(a).child("user").child('h_address').get().val()

    phno = db.child("users1").child(a).child("user").child('phone').get().val()
    vacc = db.child("hospitals").child(Hospital).child('vaccine').get().val()
    mylist = ", ".join(vacc)

    return render(request, "addprofile.html",{'Hn': Hospital, 'eml': email, 'add': address, 'phn': phno,'vac':mylist})



#LOGOUT
def logout(request):
      try:
          del request.session['uid']
      except:
           pass
      return render(request,'login.html')


# REGISTRATION
def postsignup(request):
         hname = request.POST.get('Hname')
         heml = request.POST.get('Email')
         husername = request.POST.get('Username')
         hpassw = request.POST.get('Password')
         hcpassw = request.POST.get('Confirmpassword')
         hcountry = request.POST.get('Country')
         hstate = request.POST.get('State')
         hadd = request.POST.get('Address')
         hpincode = request.POST.get('Pin')
         hphno = request.POST.get('ContactNo')


         # params = {'sensor': 'false', 'address': 'Mountain View, CA'}
         # r = requests.get(url, params=params)
         # results = r.json()['results']
         # location = results[0]['geometry']['location']
         # location['lat'], location['lng']
         #
         # g = geocoder.google('Mountain View, CA')
         # print ("--->>", g.latlng)

         try:
               user = authe.create_user_with_email_and_password(heml, hpassw)
               uid = user['localId']

               address={"address":hadd,"Email":heml,"Phone":hphno,"Country":hcountry,"State":hstate}
               lat={"lat":26.938090,"lng":75.801870}
               data={"h_name":hname,"phone":hphno,"pincode":hpincode,"username":husername,"password":hpassw ,"h_email": heml,"h_address":hadd}


               # hospital database
               db.child("hospitals").child(hname).set(address)
               db.child("hospitals").child(hname).child("location").set(lat)

                 # user database
               db.child("users1").child(uid).child("user").set(data)


         except:
            message = "Unable to create account try again"
            return render(request, "regi.html", {"messg": message})

         return render(request, "login.html")


# AFTER LOGIN ADD INFO ABOUT DISEASE AND VACCINE
# def postaftersign(request):
#     harc=request.POST.get('acr')
#     hspc=request.POST.get('special')
#     hfac=request.POST.get('fac')
#     hdis = request.POST.get('Dis')
#     hvacc = request.POST.get('Vac')
#     hvacc1 = request.POST.get('Vac1')
#     hprev=request.POST.get('preventions')
#     hprev1 = request.POST.get('preventions1')
#     hprev2 = request.POST.get('preventions2')
#     hsymp=request.POST.get('symp')
#     hsymp1 = request.POST.get('symp1')
#     hsymp2 = request.POST.get('symp2')
#
#
#     idtoken = request.session['uid']
#     a = authe.get_account_info(idtoken)
#     a = a['users']
#     a = a[0]
#     a = a['localId']
#
#
#     p=[hprev,hprev1,hprev2]
#     s=[hsymp,hsymp1,hsymp2]
#     lat = {"lat": 22.973423, "lng": 78.656891}
#     v=[hvacc,hvacc1]
#
#
#     #display vaccine in hospital
#     hname = db.child("users1").child(a).child("user").child('h_name').get().val()
#     hcon=db.child("hospitals").child(hname).child('Country').get().val()
#     db.child("hospitals").child(hname).child("vaccine").set(v)
#
#     #disease database
#     db.child("diseases").child(hdis).child("places").child(hcon).set(lat)
#     db.child("diseases").child(hdis).child("precaution").set(p)
#     db.child("diseases").child(hdis).child("symptoms").set(s)
#
#
#     d={"Accredation":harc,"Speciality":hspc,"Facility":hfac}
#     db.child("users1").child(a).child("user").child("a_info").set(d)

#     return render(request, "afterlogin.html")

