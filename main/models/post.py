from django.db import models
from .user import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    liked_users = models.ManyToManyField(User, related_name="liked_posts",  blank=True)
    viewed_users = models.ManyToManyField(User, related_name="viewed_posts", blank=True)
    new_column = models.BigIntegerField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post {self.id} by {self.user.full_name}"

class Media(models.Model):
    file = models.FileField(upload_to='post_media/') 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')

    def __str__(self):
        return f"Media for Post {self.post.id}"

class Comment(models.Model):
    content = models.CharField(max_length=500) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Comment by {self.user.full_name} on Post {self.post.id}"


