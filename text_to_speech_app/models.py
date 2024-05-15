from django.db import models

from django.contrib.auth.models import AbstractUser

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
    user = models.ForiegnKey(CustomUser, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    upload_at = models.DateTimeField(auto_now_add=True)

class Audio(models.Model):
    user = models.ForiegnKey(CustomUser, on_delete=models.CASCADE)
    pdf = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    audio_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)