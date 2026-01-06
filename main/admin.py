from django.contrib import admin
from unfold.admin import ModelAdmin

from main.models import User, Post, Comment, Media, UserConfirmation


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

admin.site.register(UserConfirmation)
@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ("id", "user", "created_at")
    search_fields = ("content",)


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ("id", "user", "post", "created_at")


@admin.register(Media)
class MediaAdmin(ModelAdmin):
    list_display = ("id", "post")

