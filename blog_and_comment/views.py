from django.db.models import Q
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework import filters

from .custom_mixins import *
from .permissions import IsCreatorOrReadOnly
from .serializer import *
from .models import *


class PostViewsets(GetSerializerClassMixin, PermissionPolicyMixin,
                   viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    search_fields = ['title', 'description', 'created_by__name']

    serializer_action_classes = {
        'retrieve': PostDetails,
    }

    permission_classes_per_method = {
        'create': [IsAuthenticated],
        'update': [IsCreatorOrReadOnly],
        'partial_update': [IsCreatorOrReadOnly],
        'destroy': [IsCreatorOrReadOnly]
    }

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         self.permission_classes = [IsCreatorOrReadOnly]
    #     elif self.action in ['create']:
    #         self.permission_classes = [IsAuthenticated]
    #     else:
    #         self.permission_classes = [AllowAny]
    #     return super().get_permissions()

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


class CommentView(PermissionPolicyMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    permission_classes_per_method = {
        'create': [IsAuthenticated],
        'update': [IsCreatorOrReadOnly],
        'partial_update': [IsCreatorOrReadOnly],
        'destroy': [IsCreatorOrReadOnly]
    }

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         self.permission_classes = [IsCreatorOrReadOnly]
    #     elif self.action in ['create']:
    #         self.permission_classes = [IsAuthenticated]
    #     return super().get_permissions()

    def create(self, request, *args, **kwargs):
        author = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=author)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
