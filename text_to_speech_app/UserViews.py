from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from text_to_speech_app.text_to_speech import *
from .forms import PDFUploadForm
from .models import PDF

def user_home(request):
    form = PDFUploadForm
    return render(request, "text_to_speech_app/user_template/user_home.html", {
        "form": form,
    })



def extract_text(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = request.FILES['pdf']

            # Extract text from PDF
            
            text = extract_text_from_pdf(pdf)
            print(text)
            return HttpResponse(text)
    else:
        return HttpResponse("Method Not Allowed")