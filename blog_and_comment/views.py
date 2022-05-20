from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializer import *
from .models import *

class BlogViewsets(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        author = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=author)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
