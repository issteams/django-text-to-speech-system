from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Admin, Other, PDF, Audio, Feedback

# Register your models here.
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Admin)
admin.site.register(Other)
admin.site.register(PDF)
admin.site.register(Audio)
admin.site.register(Feedback)
