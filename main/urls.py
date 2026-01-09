from django.urls import path
from main.views import (SendCodeAPIView, CodeVerifyAPIView,ResendCodeAPIView, SignUpApiView, LoginAPIView,PostViewSet, MediaViewSet, CommentViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"posts",PostViewSet,basename="posts" )
router.register(r"medias", MediaViewSet, basename="medias")
router.register(r"comments", CommentViewSet, basename="comments")
urlpatterns = [
    path("send-code/", SendCodeAPIView.as_view()),
    path("code-verify/", CodeVerifyAPIView.as_view()),
    path("resend-code/", ResendCodeAPIView.as_view()),
    path("sign-up/", SignUpApiView.as_view()),
    path("login/", LoginAPIView.as_view()),
]
urlpatterns += router.urls
