from main.models import Post, Media, Comment
from rest_framework import serializers
from main.models import User
from .user import UserSerializer
from django.contrib.auth import get_user_model
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id","user", "content"]
        read_only_fields = ["id",]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"]=UserSerializer(instance.user).data
        data["liked_users"]=UserSerializer(instance.liked_users, many=True).data
        data["viewed_users"]=UserSerializer(instance.viewed_users, many=True).data
        data["medias"] = MediaSerializer(instance.medias, many=True).data

        return data
class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"
        extra_kwargs = {
            'post':{'write_only':True}
        }

class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "post"]
        
        

User = get_user_model()
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
        