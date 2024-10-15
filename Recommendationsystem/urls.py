"""Recommendationsystem URL Configuration

The `urlpatterns` list routes URLs to index. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function index
    1. Add an import:  from my_app import index
    2. Add a URL to urlpatterns:  path('', index.home, name='home')
Class-based index
    1. Add an import:  from other_app.index import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import index
##from . import UserDashboard
##from . import AdminDashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index.login),
    path('logout',index.logout),
    path('dologin', index.dologin),
    path('myregister', index.register),
    path('doregister',index.doregister),
    path('bmical',index.bmical),
    path('about',index.about),
    path('about_developer',index.about_developer),
    path('analyze',index.analyze),
    path('prediction',index.prediction),
    path('home',index.home),
    path('prevpred',index.prevpred),
    path('myprofile',index.myprofile),
    path('admindashboard',index.admindashboard),
    path('viewprediction',index.viewprediction),
    path('viewuser',index.viewuser),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

