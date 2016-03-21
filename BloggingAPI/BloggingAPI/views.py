from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import  *
from .serializers import *
import uuid
from rest_framework.permissions import  AllowAny
from rest_framework.decorators import detail_route
from .permissions import *
from .pagination import *
from django.db.models import Q

class AuthorViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    Endpoint: /api/author/
    Available Methods: GET
    This end point lists all the authors on the server.
    To add an author you have to register on the site.

    GET Response objects properties:
        id -  guid of the author
        host - the host server that the author resides on
        displayname - the username of the author and the name that will be displayed for an author
        url - the host url that points to the author
        friends - a list of the author's approved friends
        first_name - the first name of an author
        last_name - the last name of an author
        email - the email of an author
        bio - the bio of an author

    Endpoint: /api/author/{AUTHOR_ID}/
    Available Methods: GET, PUT
    This end point gets the specific author that has the AUTHOR_ID.
    Use this endpoint to view a specific author and to update author information.

    GET Repsonse object properties:
        id - guid of the author
        host - the host server that the author resides on
        displayname - the username of the author and the name that will be displayed for an author
        url - the host url that points to the author
        friends - a list of the author's approved friends
        github - the author's github url
        first_name - the first name of an author
        last_name - the last name of an author
        email - the email of an author
        bio - the bio of an author

    PUT Request object properties:
        github (string) - the author's github url
        first_name (string) - the first name of an author
        last_name (string) - the last name of an author
        email (string) - the email of an author
        bio (string) - the bio of an author
    """
    queryset = Author.objects.all()
    permission_classes = (AuthorPermissions,)

    def get_serializer_class(self):
        serializer_class = ViewAuthorSerializer
        if self.request.method == 'PUT':
            serializer_class = UpdateAuthorSerializer
        return serializer_class

    def get_queryset(self):
        queryset = Author.objects.all()
        displayname = self.request.query_params.get('displayname', None)

        if displayname is not None:
            queryset = queryset.filter(user__username=displayname)

        return queryset

class PostsViewSet(viewsets.ModelViewSet):
    """
    Endpoint: /api/posts/
    Available Methods: GET, POST
    This endpoint lists the posts that are currently available to the authenticated user.
    You can also create a new post for the current user.

    GET Response objects properties:
        count (Posts) - number of posts
        query - the current query
        size - the size of the page
        title - the title of the post
        source - the last place this post was
        origin - the original url of the post
        description - the description of the post
        contentType - content type of the post
        content - the text of the post
        author - the author object that wrote the post
        categories - a list of categories that the post belongs to
        count (Comments) - the number of comments that this post has
        comments - the list of comments of a post
        published - the date the post was created
        id - the guid of the post
        visibility - the visibility level of this post

    POST Request objects properties:
        title (string) - the title of the post
        source (string) - the last place this post was
        origin (string) - the original url of the post
        description (string) - the description of the post
        contentType (string) - (text/plain or text/markdown) content type of the post
        content (string) - the text of the post
        author (UUID) - (Required, takes in AUTHOR_ID) the author id that wrote the post
        categories (string array) - (list of strings) a list of categories that the post belongs to
        visibility (string) - (PUBLIC, FOAF, FRIENDS, PRIVATE, SERVERONLY) the visibility level of this post

    Endpoint: /api/posts/{POST_ID}/
    Available Methods: GET, PUT, DELETE
    This endpoint gets the specific post with the POST_ID.
    You can also update the post and delete it.

    GET Response object properties:
        title - the title of the post
        source - the last place this post was
        origin - the original url of the post
        description - the description of the post
        contentType - content type of the post
        content - the text of the post
        author - the author object that wrote the post
        categories - a list of categories that the post belongs to
        count - the number of comments that this post has
        comments - the list of comments of a post
        published - the date the post was created
        id - the guid of the post
        visibility - the visibility level of this post

    PUT Request object properties:
        title (string) - the title of the post
        source (string) - the last place this post was
        origin (string) - the original url of the post
        description (string) - the description of the post
        contentType (string) - (text/plain or text/markdown) content type of the post
        content (string) - the text of the post
        author (UUID) - (Required, takes in AUTHOR_ID) the author object that wrote the post
        categories (string array) - (list of strings) a list of categories that the post belongs to
        visibility (string) - (PUBLIC, FOAF, FRIENDS, PRIVATE, SERVERONLY) the visibility level of this post
    """
    queryset = Post.objects.all()
    permission_classes = (PostPermissions,)
    pagination_class = PostsPagination

    def get_queryset(self):
        currentUser = self.request.user.username
        #query set for public posts
        publicQuerySet = Post.objects.all().filter(visibility='PUBLIC')
        #query set for private posts (has to be the post owner)
        privateQuerySet = Post.objects.all().filter(visibility='PRIVATE', author__user__username=currentUser)
        #query set for friends
        # friendsQuerySet = Post.objects.all().filter(visibility='FRIENDS')
        #query set for friends of friends
        # friendsOfFriendsQuerySet = Post.objects.all().filter(visibility='FOAF')
        #query set for server only
        friendsOfFriendsQuerySet = Post.objects.all().filter(visibility='SERVERONLY')

        return publicQuerySet | privateQuerySet | friendsOfFriendsQuerySet

    def get_serializer_class(self):
        serializer_class = ViewPostsSerializer
        if self.request.method == 'POST':
            serializer_class = UpdatePostsSerializer
        elif self.request.method == 'PUT':
            serializer_class = UpdatePostsSerializer
        elif self.request.method == 'DELETE':
            serializer_class = UpdatePostsSerializer
        return serializer_class


# class CurrentAuthorPostsViewSet(viewsets.ModelViewSet):
#
#     queryset = Post.objects.all()
#     serializer_class = PostsSerializer
#
#
# class AuthorPostsViewSet(viewsets.ModelViewSet):
#
#     queryset = Post.objects.all()
#     serializer_class = PostsSerializer
#
	#

class PostCommentsViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Endpoint: /api/posts/{POST_ID}/comments/
    Available Methods: GET, POST
    This endpoint lists the the comments for the current post (post with the id POST_ID).
    You can also post new comments for the corresponding post.

    GET Response objects properties:
        count - number of comments
        query - the current query
        size - the size of the page
        author - the author object that wrote the comment
        comment - the text of the comment
        pubDate - the date that the comment was created
        guid - the guid of the comment

    POST Request object properties:
        author (UUID) - (Required, takes in AUTHOR_ID) the author id that wrote the comment
        comment (string) - the text of the comment
        post (UUID) - (Required, takes in POST_ID) the post id that the comment belongs to

    Endpoint: /api/posts/{POST_ID}/comments/{COMMENT_ID}/
    Available Methods: GET
    This endpoint gets the specific comment corresponding to the COMMENT_ID and POST_ID.

    GET Response object properties:
        author - the author object that wrote the comment
        comment - the text of the comment
        pubDate - the date that the comment was created
        guid - the guid of the comment
    """
    queryset = Comment.objects.all()
    pagination_class = CommentsPagination

    def get_serializer_class(self):
        serializer_class = ViewCommentSerializer
        if self.request.method == 'POST':
            serializer_class = UpdateCommentSerializer
        return serializer_class

    def get_serializer_context(self):
        return {'post_pk': self.kwargs['posts_pk']}


# view for /api/friends/
class FriendOverviewView(APIView):
    """
    Endpoint: /api/friends/
    Available Methods: GET
    This endpoint lists the friends that each author has, and is for testing
    purposes only

    GET Response object properties:
        query - the current query
        authors - the list of friends the current author has
    """

    def get(self, request, format=None):
        queryset = Author.objects.all()
        serializer = FriendDetailSerializer(queryset, many=True)
        return Response(serializer.data)

# view for /api/friends/<author-id>
class FriendDetailView(APIView):
    """
    Endpoint: /api/friends/<author-id>
    Available Methods: GET, POST
    This endpoint lists any friends that an author has.

    GET Response object properties:
        query - the current query
        authors - the list of friends the given author has

    POST Request object properties:
        query - the current query
        author - the id of the author in question
        authors - an array of Author ID's - to bechecked against
                  the author in question to determine friendship

    POST Response object properties:
        query - the current query
        author - the id of the author in question
        authors - and array of Author ID's, all of which are friends
        with the author in question, and were present on the requested
        list
    """

    def get(self,request,pk,format=None):
        queryset = Author.objects.get(id=pk)
        serializer = FriendDetailSerializer(queryset)
        return Response(serializer.data)

    def post(self, request, pk, format=None):

        queryset = Author.objects.get(id=pk)
        serializer = FriendVerifySerializer(queryset,data=request.data,partial=True,context=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# view for /api/friendrequest/
class FriendRequestViewSet(APIView):
    """
    Endpoint: /api/friendrequest/
    Available Methods: POST
    This endpoint is used to send a friendrequest to a local
    or remote author.

    POST Request object properties:
        query - the current query
        author - an object with the following properties:
                  * id - the author id
                  * host - the author host
                  * displayName - the author's display name

        friend - an object with the following properties:
                 * id - the friend's author id
                 * host - the friend's host
                 * displayName - the friend's display name
                 * url - the url where the friend is located

    POST Response object properties:
       Posting will manipulate the database, but not return any
       serialized data. A response of success will be returned
       on a successful request, otherwise the response will be
       an error message
    """

    def post(self,request,format=None):
        authorHost = request.data['author']['host']
        friendHost = request.data['friend']['host']

        # Assume local author, and thus local friend
        if (authorHost == friendHost):

            # Get Requester
            author = Author.objects.get(id=request.data['author']['id'])

            # Get Requested
            friend = Author.objects.get(id=request.data['friend']['id'])


            followingObj = Friend.objects.create(author_id = request.data['friend']['id'],
                                          host = friendHost,
                                          display_name = request.data['friend']['displayName'],
                                          url = request.data['friend']['url'])

            pendingObj = Friend.objects.create(author_id = request.data['author']['id'],
                                          host = friendHost,
                                          display_name = request.data['friend']['displayName'],
                                          url = request.data['friend']['url'])


            try:
                author.following.add(followingObj)
                friend.pendingFriends.add(pendingObj)
                return Response('OK',status = status.HTTP_200_OK)
            except:
                return Response('Error', status=status.HTTP_400_BAD_REQUEST)

        # remote request
        else:

            # We have the friend host, author is not on our server
            # Add friend object to it's pending field

            friend = Author.objects.get(id=request.data['friend']['id'])

            pendingObj = Friend.objects.create(author_id = request.data['author']['id'],
                                               host = authorHost,
                                               display_name = request.data['author']['displayName'],
                                               url = request.data['author']['url'])

            try:
                friend.pendingFriends.add(pendingObj)
                return Response('OK',status = status.HTTP_200_OK)
            except:
                return Response('Error', status=status.HTTP_400_BAD_REQUEST)


# To be called when a friend request is posted to another service
# Adds to the follow field of the local author
class AddFollowerViewSet(APIView):
    """
    Endpoint: /api/addfollower/
    Available Methods: POST
    When a friend request is made to a remote author, post
    here to add to the local author's followers field

    POST Request object properties:
        query - the current query

        author - an object with the following properties:
                  * id - the author id
                  * host - the author host
                  * displayName - the author's display name

        friend - an object with the following properties:
                 * id - the friend's author id
                 * host - the friend's host
                 * displayName - the friend's display name
                 * url - the url where the friend is located

    POST Response object properties:
       Posting will manipulate the database, but not return any
       serialized data. A response of success will be returned
       on a successful request, otherwise the response will be
       an error message
    """

    def post(self,request,format=None):

        author = Author.objects.get(id=request.data['author']['id'])

        followingObj = Friend.objects.create(author_id = request.data['friend']['id'],
                                          host = friendHost,
                                          display_name = request.data['friend']['displayName'],
                                          url = request.data['friend']['url'])

        try:
            author.following.add(followingObj)
            return Response('Success',status = status.HTTP_200_OK)
        except:
            return Response('Error', status=status.HTTP_400_BAD_REQUEST)


# view for api/friends/<friend1>/<friend2>/
class FriendQueryViewSet(APIView):
    """
    Endpoint: /api/friends/<authorid1>/<authorid2>/
    Available Methods: GET
    Used to determine the friendship of two authors,
    specified in the URL

    GET Response properties:
        query - the current query
        authors - array of author id's, specifies both
                  authors involved
        friends - a boolean, True if friends, False otherwise
    """

    def get(self, request, pk1, pk2, format=None):
        criteria1 = Q(id=pk1)
        criteria2 = Q(id=pk2)
        queryset = Author.objects.filter(criteria1 | criteria2)
        serializer = FriendQuerySerializer(queryset,data=request.data,partial=True)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /api/author/author-id/posts
class AuthorSpecificPosts(APIView):
    """
    Endpoint: /api/author/<authorid>/posts/
    Available Methods: GET
    Gets all posts made by <author-id> that are visible to the
    currently authenticated User

    GET Response properties:
        title - the title of the post
        source - the last place this post was
        origin - the original url of the post
        description - the description of the post
        contentType - content type of the post
        content - the text of the post
        categories - a list of categories that the post belongs to
        count - number of posts
        comments - the list of comments of a post
        published - the date the post was created
        id - the guid of the post
        visibility - the visibility level of this post
    """

    def get_queryset(self):
        currentUser = self.request.user.username
        #query set for public posts
        publicQuerySet = Post.objects.all().filter(visibility='PUBLIC')
        #query set for private posts (has to be the post owner)
        privateQuerySet = Post.objects.all().filter(visibility='PRIVATE', author__user__username=currentUser)
        #query set for friends
        # friendsQuerySet = Post.objects.all().filter(visibility='FRIENDS')
        #query set for friends of friends
        # friendsOfFriendsQuerySet = Post.objects.all().filter(visibility='FOAF')
        #query set for server only
        friendsOfFriendsQuerySet = Post.objects.all().filter(visibility='SERVERONLY')

        return publicQuerySet | privateQuerySet | friendsOfFriendsQuerySet

    def get(self,request,pk,format=None):
        queryset = self.get_queryset(request).filter(id=pk)
        serializer = AuthorPostSerializer(queryset,many=True)
        return Response(serializer.data)

# /api/author/author-id/friendrequests
class AuthorFriendRequests(APIView):

    def get(self,request,pk,format=None):
        queryset = Author.objects.filter(id=pk)
        serializer = ViewFriendRequestsSerializer(queryset,many=True)
        return Response(serializer.data)

# /api/author/author-id/following
class AuthorFollowing(APIView):

    def get(self,request,pk,format=None):
        queryset = Author.objects.filter(id=pk)
        serializer = ViewFollowingSerializer(queryset,many=True)
        return Response(serializer.data)

class ConnectedNodesViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = ConnectedNodeSerializer
    queryset = Node.objects.all()

# /api/friends/acceptfriend/
class AcceptFriendViewSet(APIView):

    #POST:
    # { friend: <author_id> }

    def post(self, request, format=None):
        # Get Author
        currentUser = request.user
        author = Author.objects.all().filter(user = currentUser)
        author = author[0]
        
        friendID = request.data['friend']
        toAdd = None

        # Get friend
        for friend in author.pendingFriends.all():
            if str(friend.author_id) == str(friendID):
                toAdd = friend
                break

        if toAdd is not None:
            author.friends.add(toAdd)
            author.pendingFriends.all().filter(author_id=friendID).delete()
            print author.friends.all()
            return  Response('Success', status=status.HTTP_200_OK)
        else:
            return  Response('Friend Not Found', status=status.HTTP_400_BAD_REQUEST)

# /api/friends/removefriend/
class RemoveFriendViewSet(APIView):

    # POST:
    # { friend: <author_id> }

    def post(self, request, format=None):
        # Get Author
        currentUser = request.user
        author = Author.objects.all().filter(user = currentUser)
        author = author[0]
<<<<<<< HEAD
        
=======

>>>>>>> e3e8edd1093972a6e4b4b6459ac22a6921957489
        friendID = request.data['friend']
        toDelete = None

        # Get friend
        for friend in author.pendingFriends.all():
            if str(friend.author_id) == str(friendID):
                toDelete = friend
                break

        if toDelete is not None:
            author.Friends.all().filter(author_id=friendID).delete()
            return  Response('Success', status=status.HTTP_200_OK)
        else:
            return  Response('Friend Not Found', status=status.HTTP_400_BAD_REQUEST)
