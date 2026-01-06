from django.urls import path
from main.views import SendCodeAPIView, CodeVerifyAPIView, ResendCodeAPIView, SignUpApiView, LoginAPIView
urlpatterns = [
    path("send-code/", SendCodeAPIView.as_view()),
    path("code-verify/", CodeVerifyAPIView.as_view()),
    path("resend-code/", ResendCodeAPIView.as_view()),
    path('sign-up/', SignUpApiView.as_view()),
    path("login/", LoginAPIView.as_view()),

]   