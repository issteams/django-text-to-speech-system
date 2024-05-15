from . import views, AdminViews
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('doLogin/', views.doLogin, name='doLogin'),

    # Admin path
    path('admin_home', AdminViews.admin_home, name='admin_home'),
    


    path('logout', views.user_logout, name='logout'),
]
