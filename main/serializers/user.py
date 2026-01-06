from rest_framework import serializers
from main.models import User, NEW
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, attrs):
        email = attrs.lower().strip()
        if not email.endswith("@gmail.com"):
            raise serializers.ValidationError("Domenda xatolik bor!")
        user =  User.objects.filter(email=email).first()
        if user  and user.status!=NEW :
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
    
class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password1 = serializers.CharField(max_length=40)
    password2 = serializers.CharField(max_length=40)
    username = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=30)
    
    def validate_password(self, attrs):
        password1 = self.get('password1')
        password2 = self.get('password2')

        if password1!=password2:
            raise serializers.ValidationError("Parollar mos emas!")
    
        return super().validate(attrs)
