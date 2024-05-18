from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from text_to_speech_app.text_to_speech import *
from .forms import PDFUploadForm
from .models import PDF, Audio

def user_home(request):
    form = PDFUploadForm()
    return render(request, "text_to_speech_app/user_template/user_home.html", {
        "form": form,
    })



def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf']
            if pdf_file:
                pdf_instance = PDF(user=request.user, file=pdf_file)
                pdf_instance.save()

                # Extract text from PDF
                pdf_path = pdf_instance.file.path
                text = extract_text_from_pdf(pdf_path)

                # Convert text to audio
                audio_path = convert_text_to_audio(text, pdf_instance.id)

                # Save audio file information
                audio = Audio(user=request.user, pdf=pdf_instance, file=audio_path)
                audio.save()

                return redirect('user_home')
    else:
        form = PDFUploadForm()
    return render(request, 'text_to_speech_app/user_template/user_home.html', {'form': form})

def converted_audios(request):
    audios = Audio.objects.filter(user=request.user)
    return render(request, "text_to_speech_app/user_template/converted_audios.html", {
        "audios": audios,
    })
       