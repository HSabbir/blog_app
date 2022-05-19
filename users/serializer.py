from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import *
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

User = get_user_model()


class RegistrationSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=100)
    password= serializers.CharField()

class OtpVerificationSerializer(FriendlyErrorMessagesMixin, serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()