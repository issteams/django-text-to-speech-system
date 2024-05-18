from django import forms
from .models import PDF

class PDFUploadForm(forms.Form):
    pdf = forms.FileField(label="Upload PDF",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))
