from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Otp
from users.send_mail import send_otp_via_mail
from users.serializer import RegistrationSerializer, OtpVerificationSerializer, ForgotPasswordSerializer, \
    PasswordResetSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def register(request):
    try:
        payload = request.data
        data_serializer = RegistrationSerializer(data=payload)
        if data_serializer.is_valid():
            user_instance = User.objects.create(
                email=data_serializer.data.get('email'),
                name=data_serializer.data.get('name'),

            )
            try:
                validate_password(data_serializer.data.get('password'),user_instance)
            except Exception as e:
                return Response({
                    "code": 401,
                    "message": str(e),
                })

            password = make_password(data_serializer.data.get('password'))
            user_instance.password = password
            user_instance.save()

            send_otp_via_mail("Your Account Verification OTP",data_serializer.data.get('email'),'AA')

            return Response({
                'code': status.HTTP_200_OK,
                'message': 'User created successfully! Please verify email',
                'data': {
                    "email":data_serializer.data.get('email'),
                    "name":data_serializer.data.get('name')
                }
            })
        else:
            return Response(data_serializer.errors)

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': str(e)
        })

@api_view(['POST'])
def verify_email(request):
    try:
        data = request.data
        serializer = OtpVerificationSerializer(data=data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.data.get('email'))
            if not user.exists():
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid email'
                })

            user = user.first()
            otp = Otp.objects.filter(user=user,otp_type='AA',has_used=False).first()

            if not otp.otp == serializer.data.get('otp'):
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Wrong otp'
                })
            user.is_active = True
            user.verified = True
            otp.has_used = True
            user.save()
            otp.save()
            return Response({
                'code': 200,
                'message': 'Verified successfully'
            })

    except:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Something went wrong',
            'data': serializer.errors
        })

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    serializer = ForgotPasswordSerializer(data=data)
    if serializer.is_valid():
        try:
            email = serializer.data.get('email')
            user = User.objects.filter(email=email).first()

            send_otp_via_mail("Your OTP for password reset",user.email,'RP')
            return Response({
                "code": 200,
                "message": "Password reset OTP send in mail"
            })

        except:
            return Response({
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "No user with this email, Please Enter correct email"
            })

    return Response({
        "code": 401,
        "error": serializer.errors
    })

@api_view(['POST'])
def check_forgot_password_otp(request):
    data = request.data
    serializer = OtpVerificationSerializer(data=data)
    if serializer.is_valid():
        try:
            email = serializer.data.get('email')
            user = User.objects.filter(email=email).first()
            otp_obj = Otp.objects.filter(user=user,otp_type='RP',has_used=False).first()
            otp = serializer.data.get('otp')

            if not otp_obj.otp == otp :
                return Response({
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "message": "Wrong OTP for this email"
                })

            otp_obj.has_used=True
            otp_obj.save()
            return Response({
                "code": 200,
                "message": "Correct OTP, please enter new password"
            })

        except:
            return Response({
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "No user with this email, Please Enter correct email"
            })

    return Response({
        "code": 401,
        "error": serializer.errors
    })

@api_view(['POST'])
def reset_password(request):
    data = request.data
    serializer = PasswordResetSerializer(data=data)
    if serializer.is_valid():
        try:
            email = serializer.data.get('email')
            user = User.objects.filter(email=email).first()

            try:
                validate_password(serializer.data.get('password'),user)
            except Exception as e:
                return Response({
                    "code": 401,
                    "message": str(e),
                })

            password = make_password(serializer.data.get('password'))
            user.password = password
            user.save()

            return Response({
                "code": 200,
                "message": "Password reset successfully"
            })

        except:
            return Response({
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "No user with this email, Please Enter correct email"
            })

    return Response({
        "code": 401,
        "error": serializer.errors
    })