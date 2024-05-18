from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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


def user_logout(request):
    logout(request)
    return redirect("/")



