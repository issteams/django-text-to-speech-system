from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        print(modulename)
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "text_to_speech_app.AdminViews":
                    pass
                elif modulename == "text_to_speech_app.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites" or modulename == "django.contrib.admin.options":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "text_to_speech_app.UserViews":
                    pass
                elif modulename == "text_to_speech_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("user_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("index") or request.path == reverse("doLogin") or modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites" or modulename=="text_to_speech_app.views":
                pass
            else:
                return HttpResponseRedirect(reverse("index"))