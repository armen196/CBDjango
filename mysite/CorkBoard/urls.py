from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("addUser/", views.addUser, name="addUser"),
    path("signIn/", views.verifyLogin, name="verifyLogin")
]