from django.urls import path
from main.views import SendCodeAPIView, CodeVerifyAPIView, ResendCodeAPIView, UserAPIView
urlpatterns = [
    path("send-code/", SendCodeAPIView.as_view()),
    path("code-verify/", CodeVerifyAPIView.as_view()),
    path("resend-code/", ResendCodeAPIView.as_view()),
    path('user-change/', UserAPIView.as_view()),

]