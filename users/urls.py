from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

urlpatterns = [
    path('api/user-register/', register),
    path('api/verify_email/',verify_email),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/forgot_passowd/',forgot_password),
    path('api/check_forgot_password_otp/',check_forgot_password_otp),
    path('api/reset_password/',reset_password),
]
