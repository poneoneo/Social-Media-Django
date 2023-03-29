"""Mapping of urls to a specific view of core app"""
from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout, name="logout"),

]
