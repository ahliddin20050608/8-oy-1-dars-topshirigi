from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from config.settings import DEFAULT_FROM_EMAIL
import random
import string
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def send_code(email:str, code:str):         
    text = f"Sizni TwitterAPI ga ro'yxatdan o`tishingiz uchun tasdiqlash kodingiz: {code}"
    send_mail(
        subject="Verification codes",
        from_email = DEFAULT_FROM_EMAIL,
        message = text,
        recipient_list= [email, ],
        fail_silently=False
    )
   

def generate_pin(size=6, chars = string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

 
class CustomResponse():
    @staticmethod
    def succes(message, data=None):
        response = {
            "status":True,
            "message":message,
            "data":data
        }
        
        return Response(data=response, status=status.HTTP_200_OK)
    
    @staticmethod
    def error(message, data=None):
        response = {
            "status":False,
            "message":message,
            "data":data
        }
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    
def is_email(email):
    return re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

def is_phone(phone):
    return re.fullmatch(r'^\+?\d{10,15}$', phone)