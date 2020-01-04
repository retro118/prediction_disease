from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def map(request, *args, **kwargs):
        return render(request,"map.html",{})

def login(request, *args, **kwargs):
        return render(request,"login.html",{})