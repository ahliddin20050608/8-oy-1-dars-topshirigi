from rest_framework import serializers
from .models import User
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, attrs):
        email = attrs.lower().strip()
        if not email.endswith("@gmail.com", "@yahoo.com"):
            raise serializers.ValidationError("Domenda xatolik bor!")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Bu email allaqachon ro'yxatdan o'tgan")
        return email
class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=30)
    
    
    def validate_code(self, attrs):
        if not attrs.isdigit():
            raise serializers.ValidationError("Code faqat raqamlardan iborat bo'lishi kerak!")
        if len(attrs)!=6:
            raise serializers.ValidationError('Code 6 xonali bolishi kerak')
        return attrs
    