from rest_framework import serializers
from main.models import User, NEW, DONE
from main.utils import is_email, is_phone



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
    
class SigUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    phone = serializers.CharField(max_length=30, required=True)
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=40, required=True)
    confirm_password = serializers.CharField(max_length=40, required=True)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already in used.")
        return value
    
    def validate_phone(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Phone number already in used.")
        return value
    
    def validate(self, validated_data):
        password = validated_data.get("password")
        confirm_password = validated_data.get("confirm_password")
        
        if password != confirm_password:
            return serializers.ValidationError("Parollar mos emas!")
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)
    
    def validate(self, validate_data):
        user_input = validate_data.get("user_input")
        password = validate_data.get("password")

        if is_email(user_input):
            user = User.objects.filter(email=user_input, status=DONE).first()
            if user is None:
                raise serializers.ValidationError("User not found.")
        
        elif is_phone(user_input):
            user = User.objects.filter(phone=user_input, status=DONE).first()
            if user is None:
                raise serializers.ValidationError("User not found.")

        else:
            user = User.objects.filter(username=user_input, status=DONE).first()
            if user is None:
                raise serializers.ValidationError("User not found.")
        if not user.check_password(password):
            raise serializers.ValidationError("Password is incorrect.")
        validate_data['username'] = user.username

        return validate_data
