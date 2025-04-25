# tweetapp/utils.py
import random
from django.core.mail import send_mail
from .models import EmailOTP

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_to_user(user):
    otp = generate_otp()
    EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})
    send_mail(
        'Your OTP Code',
        f'Your OTP for uploading your audio tweet is: {otp}',
        'noreply@yourdomain.com',
        [user.email],
        fail_silently=False,
    )
