from django.contrib import admin
from .models import *

class BlogAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'blog_status','created_by','created_at']

admin.site.register(Blog,BlogAdmin)
