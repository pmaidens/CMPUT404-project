from rest_framework import serializers
from .models import *

#Author Serializer
class AuthorSerializer(serializers.ModelSerializer):

    display_name = serializers.CharField(source='Author.username')
    id = serializers.UUIDField(source='Author.uuid')

    class Meta:
        model = Author
        fields = ('id', 'host' 'display_name', 'url', 'github')

#Post Serializer
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

#Comment Serializer
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
