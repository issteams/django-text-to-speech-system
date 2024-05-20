from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Other

# Create your views here.
def index(request):
    return render(request, "text_to_speech_app/login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return redirect('admin_home')
            else:
                return redirect("user_home")
        else:
            messages.error(request,"Invalid Login Details")
            return redirect("/")

def signup(request):
    return render(request, "text_to_speech_app/signup.html")

def doUserSignup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name= request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            other_model = Other.objects.create(admin=user, address=address)
            user.save()
            messages.success(request, f"Welcome {request.username}")
            return redirect("user_home")
        except:
            messages.error(request, "Failed to Sign Up")
            return redirect("user_home")
    else:
        return HttpResponse("<h1>Method not Allowed</h1>")


def user_logout(request):
    logout(request)
    return redirect("/")



