from django.shortcuts import render


def admin_home(request):
    return render(request, "text_to_speech_app/admin_templates/admin_home.html", {})
    