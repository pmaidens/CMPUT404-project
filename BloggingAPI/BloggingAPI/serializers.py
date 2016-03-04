from rest_framework import serializers
from .models import *

#Serializers for Author
class AuthorFriendSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friend
        fields = ('id', 'host', 'display_name', 'url')

class AuthorSerializer(serializers.ModelSerializer):

    displayname = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    friends = AuthorFriendSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayname', 'url', 'friends', 'github',
          'first_name', 'last_name', 'email', 'bio')

#Serializers for Posts
class PostAuthorSerializer(serializers.HyperlinkedModelSerializer):

    displayname = serializers.CharField(source='user.username')

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayname', 'url', 'github')

class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostsSerializer(serializers.ModelSerializer):

    count = serializers.SerializerMethodField()
    comments = PostCommentSerializer(many=True, read_only=True)
    author = PostAuthorSerializer()

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'contentType',
          'content', 'author', 'categories', 'count', 'comments', 'date_created',
          'id', 'visibility')


    def get_count(self, obj):
        if obj.comments == None:
            return 0
        return obj.comments.count()

#Serializer for Comments
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
