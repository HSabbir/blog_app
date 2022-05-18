from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializer import RegistrationSerializer
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
            user_instance.set_password(data_serializer.data.get('password'))

            user_instance.save()

            # send_otp_via_mail("Your Account Verification OTP",data_serializer.data.get('email'))

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
