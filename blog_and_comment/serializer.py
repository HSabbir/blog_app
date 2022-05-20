from rest_framework import serializers

from .models import *
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin


class BlogSerializer(FriendlyErrorMessagesMixin,serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField('get_creator')

    def get_creator(self,obj):
        return obj.created_by.email

    class Meta:
        model = Blog
        fields = ['title','description','blog_status',
                  'created_at','updated_at','created_by']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by' : {'read_only': True}
        }