from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsCreatorOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializer import *
from .models import *
from .custom_mixins import GetSerializerClassMixin


class PostViewsets(GetSerializerClassMixin,viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    serializer_action_classes = {
        'retrieve': PostDetails,
    }

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsCreatorOrReadOnly]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_queryset(self, *args, **kwargs):
        current_user = self.request.user
        return Post.objects.filter(Q(created_by=current_user.id) | Q(status='PB'))

    def create(self, request, *args, **kwargs):
        author = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=author)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentView(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                viewsets.GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsCreatorOrReadOnly]
        elif self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        author = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=author)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
