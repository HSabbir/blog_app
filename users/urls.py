from django.urls import path
from .views import *

urlpatterns = [
    path('api/user-register/', register),
    path('api/verify_email/',verify_email)
]
