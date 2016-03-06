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
#This serializer is to show the nested author object in a GET request
class PostAuthorSerializer(serializers.HyperlinkedModelSerializer):

    displayname = serializers.CharField(source='user.username')

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayname', 'url', 'github')

#This serializer is to show the nested comment objects in a GET request
class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

#This serializer is for displaying posts in the API
class ViewPostsSerializer(serializers.ModelSerializer):

    count = serializers.SerializerMethodField()
    comments = PostCommentSerializer(many=True, read_only=True)
    #For GET request show the author object
    author = PostAuthorSerializer(read_only=True)
    published = serializers.DateTimeField(source='date_created')

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'contentType',
          'content', 'author', 'categories', 'count', 'comments', 'published',
          'id', 'visibility')


    def get_count(self, obj):
        if obj.comments == None:
            return 0
        return obj.comments.count()

#This serializer is for creating or editing posts in the API
class UpdatePostsSerializer(serializers.ModelSerializer):

    published = serializers.DateTimeField(source='date_created')

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'contentType',
          'content', 'author', 'categories', 'published',
          'id', 'visibility')


#Serializer for Comments
#This serializer is for viewing comments of a post
class ViewCommentSerializer(serializers.ModelSerializer):

    guid = serializers.UUIDField(source='id')
    author = PostAuthorSerializer(read_only=True)
    pubDate = serializers.DateTimeField(source='date_created')

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'pubDate', 'guid')

#This serializer is for creating and editing a comment of a post
class UpdateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('author', 'comment')
