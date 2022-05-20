from django.contrib import admin
from django.urls import path, include

from .views import PostViewsets,CommentView
from rest_framework import routers


router = routers.DefaultRouter()

router.register('post',PostViewsets)
router.register('comment',CommentView)

urlpatterns = [
    path('', include(router.urls)),
]