from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
import uuid
import random  

NEW, VERIFIED, DONE = "new", "verified", "done"


def generate_pin(length=6):
    return ''.join(random.choices('0123456789', k=length))


class User(AbstractUser):
    STATUS_CHOICES = (
        (NEW, NEW),
        (VERIFIED, VERIFIED),
        (DONE, DONE),
    )

    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="users/", blank=True, null=True)
    email = models.EmailField(unique=True)

    def create_code(self):
        code = generate_pin()
        UserConfirmation.objects.create(
            user=self,
            code=code
        )
        return code
    
    def save(self, *args, **kwargs):
        if not self.username:
            user_uuid = str(uuid.uuid4()).split("-")[-1]
            username = f"username-{user_uuid}"
            self.username = username
        if not self.password:
            random_uuid = str(uuid.uuid4()).split("-")[-1]
            password = f"password-{random_uuid}"
            self.set_password(password) 
        super().save(*args, **kwargs) 
    
    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {"access":str(refresh.access_token), "refresh":str(refresh)}
    
    
class UserConfirmation(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confirmations")
    expired_at = models.DateTimeField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk: 
            self.expired_at = timezone.now() + timezone.timedelta(minutes=2)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        if self.expired_at:
            return self.expired_at < timezone.now()
        return False
    
    def __str__(self):
        return f"{self.user.username} | {self.code}"
        
    