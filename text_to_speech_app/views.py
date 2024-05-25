from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, Other
from .forms import CreateUserForm

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
    form = CreateUserForm()
    return render(request, "text_to_speech_app/signup.html", {
        "form": form
    })

def doUserSignup(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']          
            profile_pic = request.FILES['profile_pic']

            try:
                user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, user_type=2)
                user.other.profile = profile_pic
                user.save()
                login(request, user)
                messages.success(request, f"Welcome {user.username}")
                return redirect("user_home")
            except:
                messages.error(request, "Failed to Sign Up")
                return redirect("index")
        else:
            pass
        
    else:
        return HttpResponse("<h1>Method not Allowed</h1>")


def user_logout(request):
    logout(request)
    return redirect("/")



