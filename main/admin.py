from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import User, Post, Comment, Media, PostLike, PostView


@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "status",
        "is_active",
        "is_staff",
    )
    list_filter = ("status", "is_active", "is_staff")
    search_fields = ("username", "email", "phone")


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ("id", "user", "created_at")
    search_fields = ("content",)


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ("id", "user", "post", "created_at")


@admin.register(Media)
class MediaAdmin(ModelAdmin):
    list_display = ("id", "post", "created_at")


@admin.register(PostLike)
class PostLikeAdmin(ModelAdmin):
    list_display = ("id", "user", "post", "created_at")


@admin.register(PostView)
class PostViewAdmin(ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
