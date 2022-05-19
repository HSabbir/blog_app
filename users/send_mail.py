import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from users.models import Otp

User = get_user_model()

def get_otp():
    return random.randint(1000,9999)

def send_otp_via_mail(subject,to_email,otp_type):
    otp = get_otp()
    message = f"Your otp is {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,[to_email])
    user_obj = User.objects.filter(email=to_email).first()
    otp = Otp.objects.create(user=user_obj,otp=otp,otp_type=otp_type)
    otp.save()