from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from text_to_speech_app.text_to_speech import *
from .forms import PDFUploadForm
from .models import PDF, Audio
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
    audios = Audio.objects.filter(user=request.user)
    return render(request, "text_to_speech_app/user_template/converted_audios.html", {
        "audios": audios,
    })

def uploaded_pdfs(request):
    pdfs = PDF.objects.filter(user=request.user)
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
        pdf = PDF.objects.get(id=pdf_id)
        pdf.delete()
        messages.success(request, " Pdf Deleted Successfully")
        return redirect("uploaded_pdfs")
    except:
        messages.error(request, "Failed to Delete Pdf")
        return redirect("uploaded_pdfs")

def reconvert_pdf(request, pdf_id):
    pass