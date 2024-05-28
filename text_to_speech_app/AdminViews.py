from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import CustomUser, Other, PDF, Audio, Feedback
from django.contrib import messages
from .forms import AddUserForm, ReplyForm, EditUserForm, UserProfileForm


def admin_home(request):
    total_users = CustomUser.objects.filter(user_type=2).count()
    total_active_users = CustomUser.objects.filter(is_active=True).count()
    total_uploaded_pdfs = PDF.objects.count()
    total_converted = Audio.objects.count()
    positive_feedback = Feedback.objects.filter(sentiment='positive').count()
    negative_feedback = Feedback.objects.filter(sentiment='negative').count()

    context = {
        'total_users': total_users,
        'total_active_users': total_active_users,
        'total_uploaded_pdfs': total_uploaded_pdfs,
        'total_converted': total_converted,
        'positive_feedback': positive_feedback,
        'negative_feedback': negative_feedback,
    }

    return render(request, "text_to_speech_app/admin_templates/admin_home.html", context)


def add_user(request):
    form = AddUserForm()
    return render(request, "text_to_speech_app/admin_templates/add_user_template.html", {
        "form": form,
    })

def add_user_save(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                profile_pic = request.FILES['profile_pic']

                user = CustomUser.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, user_type=2)
                
                # Assuming 'Other' is a related name in a OneToOne relationship to the CustomUser model
                user.other.profile_pic = profile_pic
                user.other.save()  # Save the related model after assigning the profile picture
                
                messages.success(request, "User Created Successfully")
                return redirect("add_user")
            except Exception as e:
                messages.error(request, f"Failed to create User: {e}")
                return redirect("add_user")
        else:
            # Return the form with validation errors
            return render(request, "text_to_speech_app/admin_templates/add_user_template.html", {
                "form": form,
            })
    else:
        # If the request is GET, render the empty form
        form = AddUserForm()
        return render(request, "text_to_speech_app/admin_templates/add_user_template.html", {
            "form": form,
        })

def manage_users(request):
    users = Other.objects.all()
    return render(request, "text_to_speech_app/admin_templates/manage_user_template.html", {
        'users': users,
    })

def edit_user(request, id):
    user = Other.objects.get(admin=id)
    form = UserProfileForm()
    form.fields['email'].initial=user.admin.email
    form.fields['first_name'].initial=user.admin.first_name
    form.fields['last_name'].initial=user.admin.last_name
    form.fields['username'].initial=user.admin.username
    return render(request, "text_to_speech_app/admin_templates/edit_user_template.html", {
        "form": form,
    })

def edit_user_save(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            if request.FILES.get('profile_pic',False):
                profile_pic = request.FILES['profile_pic']
            else:
                profile_pic = None
            try:
                user = CustomUser.objects.get(id=request.user.id)
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                if password != None and password != "":
                    user.set_password(password)
                user.save()

                other_model = Other.objects.get(admin=user)
                if profile_pic != None:
                    other_model.profile_pic = profile_pic
                other_model.save()
                messages.success(request,"Successfully Updated Profile")
                return redirect("profile")
            except:
                messages.error(request,"Failed to Update Profile")
                return redirect("profile")
        else:
            form= UserProfileForm(request.POST)
            return render(request, "text_to_speech_app/user_template/profile.html", {
                "form": form,
            })
    else:
        return HttpResponse("Method not allowed")

def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        user.delete()
        messages.success(request, f"{user.username} Deleted Successfully")
        return redirect("manage_users")
    except:
        messages.error(request, f"Failed to delete {user.usrename}")

def active_users(request):
    users = CustomUser.objects.filter(is_active=True)
    return render(request, "text_to_speech_app/admin_templates/active_users.html", {
        'users': users,
    })

def total_uploaded_pdfs(request):
    pdfs = PDF.objects.all()
    return render(request, "text_to_speech_app/admin_templates/total_uploaded_pdfs.html", {
        'pdfs': pdfs,
    })

def total_converted_audios(request):
    audios = Audio.objects.all()
    return render(request, "text_to_speech_app/admin_templates/total_converted_audios.html", {
        'audios': audios,
    })

def feedbacks(request):
    user_feedbacks = Feedback.objects.all()
    return render(request, "text_to_speech_app/admin_templates/user_feedbacks.html", {
        'user_feedbacks': user_feedbacks,
    })


@require_POST
def reply_feedback(request):
    form = ReplyForm(request.POST)
    if form.is_valid():
        feedback_id = form.cleaned_data['feedback_id']
        reply_message = form.cleaned_data['reply_message']
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.reply = reply_message
        feedback.replied = True  # Mark feedback as replied
        feedback.save()
        messages.success(request, "Reply sent successfully")
    else:
        messages.error(request, "Failed to send reply")
    return redirect('user_feedbacks')  # Change 'user_feedbacks' to your feedback listing URL name



    

