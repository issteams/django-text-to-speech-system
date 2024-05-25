from django import forms
from .models import PDF, Feedback


class CreateUserForm(forms.Form):
    first_name=forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"First Name", "style": "margin-bottom:10px;"}))
    last_name=forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Last Name", "style": "margin-bottom:10px;"}))
    email=forms.EmailField(label="",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off", "placeholder":"Email", "style": "margin-bottom:10px;"}))
    username=forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off", "placeholder":"Username", "style": "margin-bottom:10px;"}))
    profile_pic=forms.FileField(label="",max_length=50,widget=forms.FileInput(attrs={"class":"form-control", "placeholder":"Profile Pic", "style": "margin-bottom:10px;"}), required=False)
    password=forms.CharField(label="",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder":"Password"}))


class AddUserForm(forms.Form):
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"First Name"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Last Name"}))
    email=forms.EmailField(label="Email Address",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off", "placeholder":"Email"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off", "placeholder":"Username"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control", "placeholder":"Profile Pic"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder":"Password"}))

class EditUserForm(forms.Form):
    user_id = forms.HiddenInput()
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "autocomplete":"off"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}), required=False)


class UserProfileForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control", "autocomplete":"off", "placeholder":"Fill Only if You Want to change Password"}), required=False)
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}), required=False)


class PDFUploadForm(forms.Form):
    pdf = forms.FileField(label="",max_length=100,widget=forms.FileInput(attrs={"class":"form-control"}),required=True)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class ReplyForm(forms.Form):
    feedback_id = forms.IntegerField(widget=forms.HiddenInput())
    reply_message = forms.CharField(widget=forms.Textarea, required=True)