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
        reader = PyPDF2.PdfReader(file)  # Create a PDF reader object
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]  # Get each page
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

#Example usage
# pdf_path = "test.pdf"
# output_audio_path = "output_audio.mp3"
# pdf_to_audio(pdf_path, output_audio_path)