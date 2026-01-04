from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import send_code
from .serializers import EmailSerializer, CodeSerializer
from .models import User, UserConfirmation, VERIFIED, NEW
from rest_framework import status


class SendCodeAPIView(APIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email}
        )

        UserConfirmation.objects.filter(user=user).delete()

        confirmation = UserConfirmation.objects.create(
            user=user,
            code=send_code(email=email)
        )

        return Response({
            "status": True,
            "message": "Verification code has been sent",
            "token": user.token()
        }, status=status.HTTP_200_OK)
        
        
class CodeVerifyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data["code"]
        user = request.user

        if self.verify_user(user, code):
            return Response({
                "status": True,
                "message": "User verified successfully"
            }, status=200)

        return Response({
            "status": False,
            "message": "Code expired or incorrect"
        }, status=400)

    def verify_user(self, user, code):
        confirmation = user.confirmations.order_by("-created_at").first()

        if not confirmation:
            return False

        if confirmation.is_expired():
            return False

        if confirmation.code != code:
            return False

        user.status = VERIFIED
        user.save()
        confirmation.delete()
        return True

class ResendCodeAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        user = request.user
        
        if self.resend_code(user):
            data = {
                "status":True,
                "message":"Verification code resent successfully"
            }
        else:
            data = {
                "status":False,
                "message":"You have got unexpired code or You have already VERIFIED "
            }
        return Response
    
    def resend_code(self, user):
        confirmation = user.confirmation.order_by("-created_at").first()
        if confirmation.is_expired() and user.status==NEW:
            code = user.create_code()
            send_code(user.email, code)
            return True