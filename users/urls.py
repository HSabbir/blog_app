from django.urls import path
from .views import *

urlpatterns = [
    path('api/user-register/', register),
]
