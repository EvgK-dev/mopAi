from django.urls import path
 
from .views import *
from . import views
 
urlpatterns = [
    path('', mainpage, name='mainpage'), 
    path('extract_audio/', views.extract_audio, name='extract_audio'),
    path('extract_photo/', views.extract_photo, name='extract_photo'),
    path('extract_pdf/', views.extract_pdf, name='extract_pdf'),

    path("delete_ip_record/", delete_ip_record, name="delete_ip_record"),
    path('check_upload_status/', views.check_upload_status, name='check_upload_status'),
]