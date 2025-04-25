from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_audio, name='upload'),
    path('success/', views.upload_success, name='success'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]
