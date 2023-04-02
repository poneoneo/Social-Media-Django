from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from django.http.response import HttpResponse
# from django.http import HttpResponseForbidden


#Exiger que l'utlisateur soit connecte avant de d'accerder a la page d'acceuille
@login_required(login_url="core:signin")
def index(request):
    return render(request, "core/index.html")

#vue pour l'inscription des utilisateurs
def signup(request):
    #Recuperation de toutes les donnees de la requete 
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        #On verifie que les mots de passe sont identiques
        if password == password2:
            #si l'email existe
            if User.objects.filter(email=email).exists():
                info = HttpResponse(status = 401)
                data = {"info":info}
                messages.info(
                    request,
                    f"Un nom d'utilisateur est deja enregistrer avec cette email  ",
                )
                return redirect("/signup")

            #si le nom d'utilisateur existe 
            elif User.objects.filter(username=username).exists():
                info = HttpResponse(status = 401).status_code
                messages.info(request, f"Ce nom d'utilisateur existe deja ")
                return redirect("/signup")

            #si non on cree un nouvel utilisateur et on l'ajoute a la table User(fourni par django)  
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()

                #authentification de l'utilisateur et connection 
                user_loggin = auth.authenticate(username = username , password = password)
                auth.login(request, user_loggin)

            
            #creation du profile de l"utisateur et connection automatique vers la page de 
            #configuration du profile
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id )
                new_profile.save()

                return redirect("/settings")
        #si les mots de passe sont identiques, redirection vers la meme page        
        else:
            
            messages.info(request, "Les mots de passes ne sont pas identiques")
            return redirect("/signup")
            
    else:
        return render(request, "core/signup.html")

#Exiger que l'utilisateur soit connecter pour acceder a la page de configuration du Profile
@login_required(login_url="core:signin")
def settings(request):

    user_set=Profile.objects.get(user=request.user)
    
    return render(request,"core/setting.html",{"user_set":user_set},)

#Vue Pour l'inscrition des utilisateur
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None :
            auth.login(request, user=user)
            
            return redirect("/settings")
        else:
            messages.info(request, "Mot de passe ou nom d'utilisateur incorrecte !")
            return redirect("/signin")
    
    else:
        return render(request, "core/signin.html")


#Exiger que l'utilisateur soit connecte avant de se connecter(evident nooorh 😁)
@login_required(login_url="core:signin")
def logout(request):
    auth.logout(request)
    return redirect("core:signin")   
