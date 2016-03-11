from rest_framework import serializers
from .models import *

#Serializers for Author
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class AuthorFriendSerializer(serializers.HyperlinkedModelSerializer):
    #hyperlinkedModelSerializer uses hyperlinks instead of p-keys
    class Meta:
        model = Friend
        fields = ('id','author_id', 'host', 'display_name', 'url')


class ViewAuthorSerializer(serializers.ModelSerializer):

    displayname = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    friends = AuthorFriendSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayname', 'url', 'friends', 'github',
          'first_name', 'last_name', 'email', 'bio')

class FriendDetailSerializer(serializers.ModelSerializer):

    query = serializers.SerializerMethodField('getQuery')
    friends = serializers.SerializerMethodField('getFriendship')
    authors = serializers.SerializerMethodField('getFriends')

    class Meta:
        model = Author
        fields = ('query','authors','friends')

    def getFriendship(self, obj):
        #obj.Author.User
        return "true".format(bool)

    def getFriends(self,obj):
        test = obj.friends.all().values('author_id')
        res = []
        for item in test:
            res.append(item.values()[0])
        return res

    def getQuery(self,obj):
        return "friends"

class UpdateAuthorSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'email', 'github', 'bio')

    def update(self, instance, validated_data):
        #save the user info
        user_data = validated_data.pop('user')
        user =  self.context['request'].user
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.update(user, user_data)
        #save the author info
        instance.github = validated_data.get('github', instance.github)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()

        return instance

#Serializers for Posts
#This serializer is to show the nested author object in a GET request
class PostAuthorSerializer(serializers.HyperlinkedModelSerializer):

    displayname = serializers.CharField(source='user.username')

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayname', 'url', 'github')


#This serializer is to show the nested comment objects in a GET request
class PostCommentSerializer(serializers.HyperlinkedModelSerializer):

    author = PostAuthorSerializer(read_only=True)
    published = serializers.DateTimeField(source='date_created')

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType', 'published', 'id')


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
    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'contentType',
              'content', 'author', 'categories', 'visibility')


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
        fields = ('author', 'comment', 'post')
