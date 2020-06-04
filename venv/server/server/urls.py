"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.map, name='map'),
    path('login.html',views.login,name='login'),
    # url('logout/',views.logout,name="log"),
    url('postsign/',views.postsign),
    url('regi.html',views.regi,name='Regi'),
    url('postsignup/',views.postsignup,name='postsignup'),
    url('profile.html',views.profile,name='prof'),
    url('profilepost/',views.profilepost,name='profilepost'),
    url('addprofile.html',views.addprofile,name='addprof'),
    url('profilepostdel/', views.profilepostdel, name='profilepostdel'),

]