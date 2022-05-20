from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

urlpatterns = [
    path('user-register/', register),
    path('verify_email/',verify_email),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('forgot_passowd/',forgot_password),
    path('check_forgot_password_otp/',check_forgot_password_otp),
    path('reset_password/',reset_password),
]
