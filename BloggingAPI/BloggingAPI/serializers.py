from rest_framework import serializers
from .models import *

#Author Serializers
class AuthorFriendSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friend
        fields = ('id', 'host', 'display_name', 'url')

class AuthorSerializer(serializers.ModelSerializer):

    display_name = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    friends = AuthorFriendSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'host', 'display_name', 'url', 'friends', 'github',
          'first_name', 'last_name', 'email', 'bio')
        read_only_fields = ('id', 'host', 'url')

#Post Serializer
class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post

#Comment Serializer
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
