from django.db import models

from django.contrib.auth.models import AbstractUser

def pdf_upload_to(instance, filename):
    return f'pdfs/{filename}'

def audio_upload_to(instance, filename):
    return f'audios/{filename}'
# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "other"))
    user_type = models.CharField(max_length=10, choices=user_type_data, default=1)


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Other(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class PDF(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="pdf")
    file = models.FileField(upload_to=pdf_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.file)
    

class Audio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="audio")
    pdf = models.ForeignKey(PDF, on_delete=models.CASCADE)
    file = models.FileField(upload_to=audio_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(s)

    