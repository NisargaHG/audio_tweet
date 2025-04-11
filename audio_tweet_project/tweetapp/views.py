# tweetapp/views.py
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AudioTweetForm
from .models import AudioTweet, EmailOTP
from .utils import send_otp_to_user
import pytz
from datetime import time

@login_required
def upload_audio(request):
    ist = pytz.timezone('Asia/Kolkata')
    current_time = now().astimezone(ist).time()

    # Allow only between 2 PM and 7 PM
    if not time(14, 0) <= current_time <= time(19, 0):
        return render(request, 'tweets/error.html', {'message': 'You can upload audio only between 2 PM and 7 PM IST.'})

    # Check if OTP is verified
    otp_verified = request.session.get('otp_verified')
    if not otp_verified:
        # Send OTP and ask for it
        send_otp_to_user(request.user)
        return render(request, 'tweets/verify_otp.html')

    if request.method == 'POST':
        form = AudioTweetForm(request.POST, request.FILES)
        if form.is_valid():
            audio = form.save(commit=False)
            audio.user = request.user
            audio.save()
            # Reset OTP verification
            request.session['otp_verified'] = False
            return redirect('success')
    else:
        form = AudioTweetForm()

    return render(request, 'tweets/upload.html', {'form': form})
# tweetapp/views.py (add this)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=request.user).first()

        if otp_obj and otp_obj.otp == otp_input:
            request.session['otp_verified'] = True
            return redirect('upload')  # Now upload is allowed
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'tweets/verify_otp.html')
# tweetapp/views.py
from django.shortcuts import render

def upload_success(request):
    return render(request, 'tweets/success.html')
