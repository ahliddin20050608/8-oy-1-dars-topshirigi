# signals.py (agar signal kerak bo'lsa)
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender='main.User')
def create_user_confirmation(sender, instance, created, **kwargs):
    """Yangi user yaratilganda avtomatik tasdiqlash kodi yaratish"""
    if created:
        from .models import UserConfirmation  
        code = ''.join(random.choices('0123456789', k=6))
        UserConfirmation.objects.create(
            user=instance,
            code=code
        )
        print(f"Yangi user uchun tasdiqlash kodi yaratildi: {code}")


@receiver(post_save, sender='main.Post')
def update_post_stats(sender, instance, created, **kwargs):
    """Post yaratilganda yoki yangilanganda statistikani yangilash"""
    if created:
        print(f"Yangi post yaratildi: {instance.id}")