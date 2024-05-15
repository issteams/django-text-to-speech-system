from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
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
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


# Python: A versatile programming language.
# PyPDF2 or pdfplumber: Libraries for extracting text from PDF files.
# gTTS (Google Text-to-Speech) or pyttsx3: Libraries for converting text to audio.
# pydub: Library for handling audio file formats.
# Tkinter (optional): For a simple GUI if needed

# import PyPDF2

# def extract_text_from_pdf(pdf_path):
#     text = ""
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfFileReader(file)
#         for page_num in range(reader.numPages):
#             page = reader.getPage(page_num)
#             text += page.extract_text()
#     return text

# # Example usage
# pdf_path = "path_to_your_pdf_file.pdf"
# text = extract_text_from_pdf(pdf_path)


# from gtts import gTTS

# def text_to_audio(text, output_audio_path):
#     tts = gTTS(text)
#     tts.save(output_audio_path)

# # Example usage
# output_audio_path = "output_audio.mp3"
# text_to_audio(text, output_audio_path)


# def chunk_text(text, chunk_size=5000):
#     return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# def text_to_audio_chunks(text, output_audio_path):
#     chunks = chunk_text(text)
#     for i, chunk in enumerate(chunks):
#         tts = gTTS(chunk)
#         temp_path = f"temp_chunk_{i}.mp3"
#         tts.save(temp_path)
#         combine_audio(temp_path, output_audio_path)

# def combine_audio(chunk_path, final_path):
#     from pydub import AudioSegment
#     import os

#     chunk_audio = AudioSegment.from_mp3(chunk_path)
#     if not os.path.exists(final_path):
#         chunk_audio.export(final_path, format="mp3")
#     else:
#         final_audio = AudioSegment.from_mp3(final_path)
#         combined = final_audio + chunk_audio
#         combined.export(final_path, format="mp3")

# # Example usage for large texts
# text_to_audio_chunks(text, output_audio_path)



import PyPDF2  # Import the PyPDF2 library to handle PDF files
from gtts import gTTS  # Import the gTTS library for text-to-speech conversion
from pydub import AudioSegment  # Import the pydub library for audio manipulation
import os  # Import os library for file operations

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from the given PDF file.
    
    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a single string.
    """
    text = ""  # Initialize an empty string to hold the extracted text
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)  # Create a PDF reader object
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)  # Get each page
            text += page.extract_text()  # Extract text from the page and add to the text string
    return text

def chunk_text(text, chunk_size=5000):
    """
    Splits the text into smaller chunks.
    
    :param text: The complete text to be chunked.
    :param chunk_size: Maximum size of each chunk.
    :return: List of text chunks.
    """
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def combine_audio(chunk_path, final_path):
    """
    Combines a chunk of audio with the final audio file.
    
    :param chunk_path: Path to the chunk audio file.
    :param final_path: Path to the final audio file.
    """
    chunk_audio = AudioSegment.from_mp3(chunk_path)  # Load the chunk audio
    if not os.path.exists(final_path):
        chunk_audio.export(final_path, format="mp3")  # Save the chunk as the final audio if it doesn't exist
    else:
        final_audio = AudioSegment.from_mp3(final_path)  # Load the existing final audio
        combined = final_audio + chunk_audio  # Combine the final audio with the chunk
        combined.export(final_path, format="mp3")  # Save the combined audio as the final audio

def text_to_audio_chunks(text, output_audio_path):
    """
    Converts large text to audio in chunks and combines them.
    
    :param text: The complete text to be converted to audio.
    :param output_audio_path: Path to save the output audio file.
    """
    chunks = chunk_text(text)  # Split the text into chunks
    for i, chunk in enumerate(chunks):
        tts = gTTS(chunk)  # Convert each chunk to audio
        temp_path = f"temp_chunk_{i}.mp3"  # Temporary file for the chunk
        tts.save(temp_path)  # Save the chunk audio
        combine_audio(temp_path, output_audio_path)  # Combine the chunk audio with the final audio
        os.remove(temp_path)  # Remove the temporary chunk file

def pdf_to_audio(pdf_path, output_audio_path):
    """
    Converts a PDF file to an audio file.
    
    :param pdf_path: Path to the PDF file.
    :param output_audio_path: Path to save the output audio file.
    """
    text = extract_text_from_pdf(pdf_path)  # Extract text from the PDF
    text_to_audio_chunks(text, output_audio_path)  # Convert text to audio in chunks

# Example usage
pdf_path = "path_to_your_pdf_file.pdf"
output_audio_path = "output_audio.mp3"
pdf_to_audio(pdf_path, output_audio_path)

