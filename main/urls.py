from django.urls import path
from .views import SendCodeAPIView, CodeVerifyAPIView, ResendCodeAPIView
urlpatterns = [
    path("send-code/", SendCodeAPIView.as_view()),
    path("code-verify/", CodeVerifyAPIView.as_view()),
    path("resend-code/", ResendCodeAPIView.as_view()),

]