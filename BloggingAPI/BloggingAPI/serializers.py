from rest_framework import serializers
from .models import *

#Author Serializer
class AuthorSerializer(serializers.ModelSerializer):

    display_name = serializers.CharField(source='Author.user.username')

    class Meta:
        model = Author
        fields = ('user', 'id', 'host', 'display_name', 'url', 'github', 'friends')

#Post Serializer
class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post

#Comment Serializer
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
