from . import views, AdminViews, UserViews
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('doLogin/', views.doLogin, name='doLogin'),
    path('doLogin/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('doUserSignup/', views.doUserSignup, name='doUserSignup'),

    # Admin path
    path('admin_home/', AdminViews.admin_home, name='admin_home'),
    path('add_user/', AdminViews.add_user, name='add_user'),
    path('add_user_save/', AdminViews.add_user_save, name='add_user_save'),
    path('manage_users/', AdminViews.manage_users, name='manage_users'),
    path('edit_user/<str:id>', AdminViews.edit_user, name='edit_user'),
    path('edit_user_save/', AdminViews.edit_user_save, name='edit_user_save'),
    path('delete_user/<str:user_id>', AdminViews.delete_user, name='delete_user'),


    # User Views
    path('user_home/', UserViews.user_home, name='user_home'),
    path('upload_pdf/', UserViews.upload_pdf, name='upload_pdf'),
    path('converted_audios/', UserViews.converted_audios, name='converted_audios'),
    path('uploaded_pdfs/', UserViews.uploaded_pdfs, name='uploaded_pdfs'),
    path('delete_audio/<str:audio_id>', UserViews.delete_audio, name='delete_audio'),
    path('delete_pdf/<str:pdf_id>', UserViews.delete_pdf, name='delete_pdf'),
    path('reconvert_pdf/<str:pdf_id>', UserViews.reconvert_pdf, name='reconvert_pdf'),

    


    path('logout', views.user_logout, name='logout'),
]
