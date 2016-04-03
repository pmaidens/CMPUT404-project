from rest_framework import serializers
from .models import *

#Serializers for Author
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class AuthorFriendSerializer(serializers.HyperlinkedModelSerializer):
    #hyperlinkedModelSerializer uses hyperlinks instead of p-keys
    id = serializers.UUIDField(source='author_id')
    class Meta:
        model = Friend
        fields = ('id', 'host', 'displayName', 'url')


class ViewAuthorSerializer(serializers.ModelSerializer):

    displayName = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    friends = AuthorFriendSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'url', 'friends', 'github',
          'first_name', 'last_name', 'email', 'bio')


# Used to serailize response for a GET to /api/friends/<auth id>
class FriendDetailSerializer(serializers.ModelSerializer):

    query = serializers.SerializerMethodField('getQuery')
    authors = serializers.SerializerMethodField('getFriends')

    class Meta:
        model = Author
        fields = ('query','authors')

    def getFriends(self,obj):
        query = obj.friends.all().values('author_id')
        res = []
        for item in query:
            res.append(item.values()[0])
        return res

    def getQuery(self,obj):
        return "friends"

# Used to serailize response for a POST to /api/friends/<auth id>
class FriendVerifySerializer(serializers.ModelSerializer):

    query = serializers.SerializerMethodField('getQuery')
    author = serializers.SerializerMethodField('getAuthor')
    authors = serializers.SerializerMethodField('parseFriendList')

    class Meta:
        model = Author
        fields = ('query','author','authors')

    def getQuery(self,obj):
        return self.context.get('query')

    def getAuthor(self,obj):
        return self.context.get('author')  # for consistency

    def parseFriendList(self,obj):
        # get all friends
        friendList = obj.friends.all().values('author_id')
        friends = []
        for item in friendList:
            friends.append(str(item.values()[0]))

        result = []
        for author in self.context.get('authors'):
            author = str(author)
            if author in friends:
                result.append(author)
        return result

# Used to tell if two authors are friends
class FriendQuerySerializer(serializers.ModelSerializer):

    query = serializers.SerializerMethodField('getQuery')
    authors = serializers.SerializerMethodField('getAuthors')
    friends = serializers.SerializerMethodField('getFriendship')

    class Meta:
        model = Author
        fields = ('query','authors','friends')

    def getQuery(self,obj):
        return "friends"

    def getAuthors(self,obj):
        res = []
        for author in obj:
            res.append(author.id)
        return res

    def getFriendship(self,obj):
        author1 = obj[0]
        author2 = obj[1]

        for friend in author1.friends.all():
            if friend.author_id == author2.id:
                return True
        return False



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

    displayName = serializers.CharField(source='user.username')

    class Meta:
        model = Author
        fields = ('id', 'host', 'displayName', 'url', 'github')

#This serializer is to show comment author object
class PostCommentAuthorSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.UUIDField(source='author_id')

    class Meta:
        model = CommentAuthor
        fields = ('id', 'host', 'displayName', 'url', 'github')

#This serializer is to show the nested comment objects in a GET request
class PostCommentSerializer(serializers.HyperlinkedModelSerializer):

    author = PostCommentAuthorSerializer(read_only=True)
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
          'id', 'visibility', 'image')


    def get_count(self, obj):
        if obj.comments == None:
            return 0
        return obj.comments.count()


#This serializer is for creating or editing posts in the API
class UpdatePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'description', 'date_created','contentType',
              'content', 'author', 'categories', 'visibility', 'image')


#Serializer for Comments
#This serializer is for viewing author of Comments
class ViewCommentAuthorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='author_id')
    class Meta:
        model = CommentAuthor
        fields = ('id', 'host', 'displayName')

#This serializer is for viewing comments of a post
class ViewCommentSerializer(serializers.ModelSerializer):

    guid = serializers.UUIDField(source='id')
    author = ViewCommentAuthorSerializer(read_only=True)
    pubDate = serializers.DateTimeField(source='date_created')

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'pubDate', 'guid')

#This serialzer is specifically creating author objects for a comment
class CommentAuthorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='author_id')

    class Meta:
        model = CommentAuthor
        fields = ('id', 'host', 'displayName', 'url', 'github')

#This serializer is for creating and editing a comment of a post
class UpdateCommentSerializer(serializers.ModelSerializer):

    author = CommentAuthorSerializer()

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'contentType')

    def create(self, validated_data):
        #create the comment author object
        commentAuthorData = validated_data.pop('author')
        author = CommentAuthor.objects.create(**commentAuthorData)
        post_id = Post.objects.get(id=self.context['post_pk'])
        comment = Comment.objects.create(post=post_id, author=author, **validated_data)
        return comment

class ViewFriendSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friend
        fields = ('author_id', 'host', 'displayName', 'url')

class ViewFriendRequestsSerializer(serializers.ModelSerializer):
    friendrequests = ViewFriendSerializer(source='pendingFriends', many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'friendrequests')

class ViewFollowingSerializer(serializers.ModelSerializer):
    following = ViewFriendSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'following')

class ConnectedNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('url', 'username', 'password')
