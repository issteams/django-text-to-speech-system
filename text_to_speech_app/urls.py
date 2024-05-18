from . import views, AdminViews, UserViews
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('doLogin/', views.doLogin, name='doLogin'),

    # Admin path
    path('admin_home/', AdminViews.admin_home, name='admin_home'),
    path('add_user/', AdminViews.add_user, name='add_user'),
    path('add_user_save/', AdminViews.add_user_save, name='add_user_save'),
    path('manage_users/', AdminViews.manage_users, name='manage_users'),
    path('edit_user/<str:id>', AdminViews.edit_user, name='edit_user'),
    path('edit_user_save/', AdminViews.edit_user_save, name='edit_user_save'),


    # User Views
    path('user_home/', UserViews.user_home, name='user_home'),
    path('extract_text/', UserViews.extract_text, name='extract_text'),

    


    path('logout', views.user_logout, name='logout'),
]
