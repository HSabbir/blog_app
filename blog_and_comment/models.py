from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Blog(models.Model):
    BLOG_STATUS_CHOICES = [
        ('PB', 'published'),
        ('DR', 'draft')
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    blog_status = models.CharField(choices=BLOG_STATUS_CHOICES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,related_name='blog_owner',on_delete=models.CASCADE)