from django.contrib import admin
from django.urls import path, include

from .views import BlogViewsets
from rest_framework import routers


router = routers.DefaultRouter()

router.register('blog',BlogViewsets)

urlpatterns = [
    path('', include(router.urls)),
]