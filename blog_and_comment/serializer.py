from rest_framework import serializers

from .models import *
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin


class PostSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField('get_creator')

    def get_creator(self, obj):
        return obj.created_by.email

    class Meta:
        model = Post
        fields = ['title', 'description', 'status',
                  'created_at', 'updated_at', 'created_by']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True}
        }


class CommentSerializer(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField('get_creator')

    def get_creator(self, obj):
        return obj.created_by.email

    class Meta:
        model = Comment
        fields = ['post','body','created_at', 'updated_at', 'created_by']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'post' : {'write_only': True}
        }

class PostDetails(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    comments = CommentSerializer(many=True,read_only=True)
    created_by = serializers.SerializerMethodField('get_creator')

    def get_creator(self, obj):
        return obj.created_by.email

    class Meta:
        model = Post
        fields = ['title', 'description', 'status',
                  'created_at', 'updated_at', 'created_by','comments']