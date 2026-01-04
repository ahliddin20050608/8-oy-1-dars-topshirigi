from django.core.mail import send_mail
from config.settings import DEFAULT_FROM_EMAIL
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserConfirmation
import random
import string

def generate_pin(size=6, chars = string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def send_code(email:str, code:str):
    text = f"Sizni TwitterAPI ga ro'yxatdan o`tishingiz uchun tasdiqlash kodingiz: {code}"
    send_mail(
        subject="Verification codes",
        from_email = DEFAULT_FROM_EMAIL,
        message = text,
        recipient_list= [email, ],
        fail_silently=False
    )