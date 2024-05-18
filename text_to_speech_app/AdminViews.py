from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser, Other, PDF, Audio
from django.contrib import messages


def admin_home(request):
    return render(request, "text_to_speech_app/admin_templates/admin_home.html", {})


def add_user(request):
    return render(request, "text_to_speech_app/admin_templates/add_user_template.html")

def add_user_save(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, user_type=2)
            # user.other.address = address
            user.save()
            messages.success(request, "User Created Successfully")
            return redirect("add_user")
        except:
            messages.error(request, "Failed to create User")
            return redirect("add_user")

    
    else:
        return redirect('add_user')

def manage_users(request):
    users = Other.objects.all()
    return render(request, "text_to_speech_app/admin_templates/manage_user_template.html", {
        'users': users,
    })

def edit_user(request, id):
    user = Other.objects.get(admin=id)
    return render(request, "text_to_speech_app/admin_templates/edit_user_template.html", {
        "user": user,
    })

def edit_user_save(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.get(id=user_id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            # Updating the other model
            other = Other.objects.get(admin=user_id)
            other.address = address
            other.save()
            messages.success(request, "User Update Sucessfully")
            return redirect("edit_user", user_id)
        except:
            messages.error(request, "Failed to update User")
            return redirect("edit_user", user_id)
    else:
        return HttpResponse("Method not Allowed") 

def audios(request):
    audios = Audio.objects.all()
    return render(request, "text_to_speech_app/admin_templates/audios_template.html", {
        "audios": audios,
    })
       