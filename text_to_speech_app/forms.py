from django import forms
from .models import PDF

class PDFUploadForm(forms.Form):
    pdf = forms.FileField(label="",max_length=100,widget=forms.FileInput(attrs={"class":"form-control"}),required=True)