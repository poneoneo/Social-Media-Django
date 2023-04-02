"""Mapping of urls to a specific view of core app"""
from django.urls import path
from . import views

#Preciser un espace de nom pour les urls de l'app "core"
app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("settings/", views.settings, name="settings"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout, name="logout"),

]
