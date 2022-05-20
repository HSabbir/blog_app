from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'status','created_by','created_at']

admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post', 'body','created_by','created_at']

admin.site.register(Comment,CommentAdmin)
