from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    POST_STATUS_CHOICES = [
        ('PB', 'published'),
        ('DR', 'draft')
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=POST_STATUS_CHOICES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='post_owner', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    created_by = models.ForeignKey(User, related_name='comment_owner', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
