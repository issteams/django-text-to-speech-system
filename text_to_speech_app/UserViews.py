from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from text_to_speech_app.text_to_speech import *
from .forms import PDFUploadForm
from .models import PDF

def user_home(request):
    return render(request, "text_to_speech_app/user_template/user_home.html", {})

def convert_text_to_audio(text, pdf_id):
    tts = gTTS(text)
    audio_path = f'audios/audio_{pdf_id}.mp3'
    audio_content = ContentFile(tts.save(), name=audio_path)
    saved_path = default_storage.save(audio_path, audio_content)
    return saved_path



def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.user = request.user
            pdf.save()

            # Extract text from PDF
            pdf_path = pdf.file.path
            text = extract_text_from_pdf(pdf_path)

            # Convert text to audio
            audio_path = convert_text_to_audio(text, pdf.id)

            # Save audio file information
            audio = Audio(pdf=pdf, file=audio_path)
            audio.save()
            print(pdf)
            print(audio)
            return redirect('profile')
    else:
        form = PDFUploadForm()
    return render(request, "text_to_speech_app/user_template/user_home.html", {
        "form": form,
    })