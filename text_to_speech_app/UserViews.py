from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from text_to_speech_app.text_to_speech import *
from .forms import PDFUploadForm, FeedbackForm, UserProfileForm
from .models import PDF, Audio, CustomUser, Other, Feedback
import os


def user_home(request):
    form = PDFUploadForm()
    return render(request, "text_to_speech_app/user_template/user_home.html", {
        "form": form,
    })



@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf']
            pdf_instance = PDF.objects.create(user=request.user, file=pdf_file)

            # Extract text from PDF
            pdf_path = pdf_instance.file.path
            text = extract_text_from_pdf(pdf_path)

            # Convert text to audio
            audio_relative_path = convert_text_to_audio(text, pdf_instance.id)
            audio_absolute_path = os.path.join(settings.MEDIA_ROOT, audio_relative_path)

            # Save audio file information
            audio_instance = Audio.objects.create(user=request.user, pdf=pdf_instance, file=audio_relative_path)
            
            response_data = {
                'message': 'PDF converted successfully!',
                'audio_url': audio_instance.file.url,
                'audio_name': audio_instance.file.name
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Invalid form'}, status=400)
    else:
        form = PDFUploadForm()
    return render(request, 'text_to_speech_app/user_template/user_home.html', {'form': form})

def converted_audios(request):
    audios = Audio.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "text_to_speech_app/user_template/converted_audios.html", {
        "audios": audios,
    })

def uploaded_pdfs(request):
    pdfs = PDF.objects.filter(user=request.user).order_by('uploaded_at')
    return render(request, "text_to_speech_app/user_template/uploaded_pdfs.html", {
        "pdfs": pdfs,
    })

def delete_audio(request, audio_id):
    try:
        audio = Audio.objects.get(id=audio_id)
        audio.delete()
        messages.success(request, "Successfully Deleted")
        return redirect("converted_audios")
    except:
        messages.error(request, "Failed to delete Audio")
        return redirect("converted_audios")

def delete_pdf(request, pdf_id):
    try:
        pdf = get_object_or_404(PDF, id=pdf_id, user=request.user)
        # Disassociate audios from this PDF before deleting the PDF
        Audio.objects.filter(pdf=pdf).update(pdf=None)
        pdf.delete()
        messages.success(request, " Pdf Deleted Successfully")
        return redirect("uploaded_pdfs")
    except:
        messages.error(request, "Failed to Delete Pdf")
        return redirect("uploaded_pdfs")

@login_required
def reconvert_pdf(request, pdf_id):
    if request.method == 'GET':
        try:
            pdf_instance = PDF.objects.get(id=pdf_id)
            audio_instance = Audio.objects.get(pdf=pdf_instance)

            # Extract text from PDF
            pdf_path = pdf_instance.file.path
            text = extract_text_from_pdf(pdf_path)

            # Convert text to audio
            audio_path = convert_text_to_audio(text, pdf_instance.id)

            # Update audio file information
            audio_instance.file.name = audio_path  # Ensure correct assignment
            audio_instance.save()

            response_data = {
                'status': 'success',
                'message': 'PDF reconverted successfully!',
                'audio_url': audio_instance.file.url,
                'audio_name': audio_instance.file.name
            }
            messages.success(request, "Successfully converted")
            return JsonResponse(response_data)

        except PDF.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'PDF not found.'}, status=404)
        except Audio.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Audio not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method or not an AJAX request.'}, status=400)

def about(request):
    return render(request, "text_to_speech_app/user_template/about.html")

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback')
    else:
        form = FeedbackForm()
        feedbacks = Feedback.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'text_to_speech_app/user_template/feedback.html', {'form': form, "feedbacks": feedbacks})

def profile(request):
    user = Other.objects.get(admin=request.user.id)
    form = UserProfileForm()
    form.fields['email'].initial=user.admin.email
    form.fields['first_name'].initial=user.admin.first_name
    form.fields['last_name'].initial=user.admin.last_name
    form.fields['username'].initial=user.admin.username
    return render(request, "text_to_speech_app/user_template/profile.html", {
        "form": form,
    })

def profile_save(request):
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

def search_pdfs(request):
    query = request.GET.get('q', '')
    pdfs = PDF.objects.filter(Q(file__icontains=query))
    results = [{'id': pdf.id, 'file': pdf.file, 'basename': os.path.basename(pdf.file.name)} for pdf in pdfs]
    return JsonResponse({'pdfs': results})

def search_audios(request):
    query = request.GET.get('q', '')
    audios = Audio.objects.filter(Q(file__icontains=query))
    results = [{'id': audio.id, 'file': audio.file.url, 'basename': os.path.basename(audio.file.name)} for audio in audios]
    return JsonResponse({'audios': results})