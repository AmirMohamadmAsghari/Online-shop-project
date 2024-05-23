import random
import json
import redis
import string
import pyotp
from .models import CustomUser
from django.core.mail import send_mail
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def generate_otp(email):
    try:
        otp = pyotp.TOTP(pyotp.random_base32(), interval=300)
        otp_code = otp.now()
        CustomUser.objects.filter(email=email).update(otp_code=otp_code)
        return otp_code
    except Exception as e:
        print(f'Error generating OTP: {e}')
        return None


def store_otp_in_redis(email, otp_code):
    print(email)
    try:
        redis_client.setex(email, 300, otp_code)
    except Exception as e:
        print(f'Error storing OTP in Redis: {e}')


def send_otp_email(email, otp_code):
    user = CustomUser.objects.get(email=email)
    send_mail(
        f'Online Shop Amir',
        f'Welcome {user.username} Your OTP Code is {otp_code}',
        'onlin.shop.project@gmail.com',
        [email],
        fail_silently=False
    )
