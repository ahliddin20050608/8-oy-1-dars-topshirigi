from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.utils import send_code, CustomResponse
from main.serializers import EmailSerializer, CodeSerializer,LoginSerializer, SigUpSerializer
from main.models import User,  VERIFIED, NEW, DONE
from rest_framework import status
from django.contrib.auth import authenticate

class SendCodeAPIView(APIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data["email"]
        user =User.objects.create(email=email)
        code = user.create_code()
        
        send_code(email=email, code=code) 

        return CustomResponse.succes(
            message="Verification code has been sent",
            data=user.token()
        )
        
        
class CodeVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        user = request.user

        if self.verify_user(user, code):
            return CustomResponse.succes(
                message="User verified successfully"
            )
            
        return CustomResponse.error(
                message= "Code already expired or incorrect"
            )

    def verify_user(self, user, code):
        confirmation = user.confirmations.order_by("-created_at").first()

        if not confirmation.is_expired() and confirmation.code ==code:
            user.status = VERIFIED
            user.save()
            return True

class ResendCodeAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        user = request.user
        
        if self.resend_code(user):
            return CustomResponse.succes(
                message="Verification code resent successfully"
            )

        return CustomResponse.error(
            message="You have got unexpired code or You have already VERIFIED "
        )
    
    def resend_code(self, user):
        confirmation = user.confirmation.order_by("-created_at").first()
        if confirmation.is_expired() and user.status==NEW:
            code = user.create_code()
            send_code(user.email, code)
            return True
        
class SignUpApiView(APIView):
    serializer_class = SigUpSerializer
    permission_classes = [IsAuthenticated,]
    
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)    
        serializer.is_valid(raise_exception=True)
         
        username = serializer.validated_data.get("username")
        phone = serializer.validated_data.get("phone")
        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name", "N/A")
        password = serializer.validated_data.get("password")
        
        if user.status==VERIFIED:
            user.username = username
            user.phone = phone
            user.first_name = first_name
            user.last_name = last_name
            user.set_password(password)
            user.status=DONE
            user.save()
            
            data = {
                "username":username,
                "phone":phone,
                "first_name":first_name,
                "last_name":last_name
            }

        
            return CustomResponse.succes(
                message='User updated succesfully.',
                data = data
            )
        return CustomResponse.error(
            message="User hasn't verified"
            
        )
        
        
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password") 
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return CustomResponse.succes(
                message="User logged in succesfully",
                data=user.token()
            )
        return CustomResponse.error(
            message="User not found"
        )