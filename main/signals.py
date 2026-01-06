import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from main.models import UserConfirmation  
from main.utils import generate_pin

import random


@receiver(post_save, sender='main.User')
def create_user_confirmation(sender, instance, created, **kwargs):
    if created:
        code = generate_pin()
        UserConfirmation.objects.create(
            user=instance,
            code=code
        )


@receiver(post_save, sender='main.Post')
def update_post_stats(sender, instance, created, **kwargs):
    if created:
        print(f"Yangi post yaratildi: {instance.id}")