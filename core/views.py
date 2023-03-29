from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from django.http.response import HttpResponse
# from django.http import HttpResponseForbidden

@login_required(login_url="core:signin")
def index(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(email=email).exists():
                info = HttpResponse(status = 401)
                data = {"info":info}
                messages.info(
                    request,
                    f"Un nom d'utilisateur est deja enregistrer avec cette email  ",
                )
                return redirect("/signup")

            elif User.objects.filter(username=username).exists():
                info = HttpResponse(status = 401).status_code
                messages.info(request, f"Ce nom d'utilisateur existe deja ")
                return redirect("/signup")
                
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
            
            #create a Profile for a new User 
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id )
                new_profile.save()
        
                messages.info(request, f"Inscription valide connectez-vous 😉 ! 🔥" )

                return redirect("/signin")
                
        else:
            
            messages.info(request, "Les mots de passes ne sont pas identiques")
            return redirect("/signup")
            
    else:
        return render(request, "core/signup.html")

@login_required(login_url="core:signin")
def settings(request):
    # username = request
    # logged_user = Profile.objects.get()
    return render(request, template_name = "core/setting.html")

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

@login_required(login_url="core:signin")
def logout(request):
    auth.logout(request)
    return redirect("core:signin")   
