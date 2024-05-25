from django.db import models

from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def classify_feedback_vader(feedback_text):
    score = analyzer.polarity_scores(feedback_text)
    if score['compound'] >= 0.05:
        return 'positive'
    elif score['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def pdf_upload_to(instance, filename):
    return f'pdfs/{filename}'

def audio_upload_to(instance, filename):
    return f'audios/{filename}'

def profile_pic_upload_to(instance, filename):
    return f'profile pics/{filename}'
# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Other"))
    user_type = models.CharField(max_length=10, choices=user_type_data, default=1)


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Other(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(upload_to=profile_pic_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class PDF(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="pdf")
    file = models.FileField(upload_to=pdf_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.file)
    

class Audio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="audio")
    pdf = models.ForeignKey(PDF, on_delete=models.SET_NULL, blank=True, null=True,)
    file = models.FileField(upload_to=audio_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(s)

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField(null=True, blank=True)
    replied = models.BooleanField(default=False)
    sentiment = models.CharField(max_length=10, choices=[('positive', 'Positive'), ('negative', 'Negative'), ('neutral', 'Neutral')], default='neutral')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.sentiment = classify_feedback_vader(self.message)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.created_at}"


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(admin=instance)
        if instance.user_type==2:
            Other.objects.create(admin=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.other.save()
    