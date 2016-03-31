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
from django.contrib.sites.models import Site

class ConnectedNodesViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = ConnectedNodeSerializer
    queryset = Node.objects.all()
    permission_classes = (IsAuthenticated, NodePermissions,)

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
        image - an image url

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
        if currentUser:
            authorFriends = Author.objects.get(user__username=currentUser).friends.all()
            #query set for public posts
            publicQuerySet = Post.objects.all().filter(visibility='PUBLIC')
            #query set for private posts (has to be the post owner)
            privateQuerySet = Post.objects.all().filter(visibility='PRIVATE', author__user__username=currentUser)
            #query set for friends
            #first get only your own 'friends' posts
            friendsQuerySet = Post.objects.filter(visibility='FRIENDS', author__user__username=currentUser)
            #next get all your friends 'friends' posts
            for friend in authorFriends:
                friendsQuerySet = friendsQuerySet | Post.objects.all().filter(visibility='FRIENDS', author__id=friend.author_id)
            #query set for friends of friends
            # friendsOfFriendsQuerySet = Post.objects.all().filter(visibility='FOAF')
            #query set for server only friends
            #first get the current user server only posts
            serverOnlyQuerySet = Post.objects.all().filter(visibility='SERVERONLY', author__user__username=currentUser)
            #next get the current user's friends that are on this server posts
            for friend in authorFriends:
                if friend.host in Site.objects.get_current().domain:
                    serverOnlyQuerySet = serverOnlyQuerySet | Post.objects.all().filter(visibility='SERVERONLY', author__id=friend.author_id)

            return publicQuerySet | privateQuerySet | friendsQuerySet | serverOnlyQuerySet

        else:
            return Post.objects.all().filter(visibility='PUBLIC')

    def get_serializer_class(self):
        serializer_class = ViewPostsSerializer
        if self.request.method == 'POST':
            serializer_class = UpdatePostsSerializer
        elif self.request.method == 'PUT':
            serializer_class = UpdatePostsSerializer
        elif self.request.method == 'DELETE':
            serializer_class = UpdatePostsSerializer
        return serializer_class

    #only list public posts for /posts endpoint
    def list(self, request):
        queryset = Post.objects.all().filter(visibility='PUBLIC')
        serializer = ViewPostsSerializer(queryset, many=True)
        return Response(serializer.data)


# /api/author/author-id/posts
class AuthorSpecificPosts(mixins.ListModelMixin, viewsets.GenericViewSet):
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
    queryset = Post.objects.all()
    pagination_class = PostsPagination

    def get_queryset(self):
        currentUser = self.request.user.username
        if currentUser:
            authorFriends = Author.objects.get(user__username=currentUser).friends.all()
            #query set for public posts
            publicQuerySet = Post.objects.all().filter(visibility='PUBLIC')
            #query set for private posts (has to be the post owner)
            privateQuerySet = Post.objects.all().filter(visibility='PRIVATE', author__user__username=currentUser)
            #query set for friends
            #first get only your own 'friends' posts
            friendsQuerySet = Post.objects.filter(visibility='FRIENDS', author__user__username=currentUser)
            #next get all your friends 'friends' posts
            for friend in authorFriends:
                friendsQuerySet = friendsQuerySet | Post.objects.all().filter(visibility='FRIENDS', author__id=friend.author_id)
            #query set for friends of friends
            # friendsOfFriendsQuerySet = Post.objects.all().filter(visibility='FOAF')
            #query set for server only friends
            #first get the current user server only posts
            serverOnlyQuerySet = Post.objects.all().filter(visibility='SERVERONLY', author__user__username=currentUser)
            #next get the current user's friends that are on this server posts
            for friend in authorFriends:
                if friend.host in Site.objects.get_current().domain:
                    serverOnlyQuerySet = serverOnlyQuerySet | Post.objects.all().filter(visibility='SERVERONLY', author__id=friend.author_id)

            return publicQuerySet | privateQuerySet | friendsQuerySet | serverOnlyQuerySet

        else:
            return Post.objects.all().filter(visibility='PUBLIC')

    def list(self, request, pk):
        queryset = self.get_queryset().filter(author__id=pk)
        serializer = AuthorPostSerializer(queryset,many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AuthorPostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


# /api/author/posts
class CurrentPostsAvailable(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Endpoint: /api/author/posts/
    Available Methods: GET
    Gets all posts that are available to the currently authenticated user.

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
    queryset = Post.objects.all()
    pagination_class = PostsPagination

    def get_queryset(self):
        currentUser = self.request.user.username
        if currentUser:
            authorFriends = Author.objects.get(user__username=currentUser).friends.all()
            #query set for public posts
            publicQuerySet = Post.objects.all().filter(visibility='PUBLIC')
            #query set for private posts (has to be the post owner)
            privateQuerySet = Post.objects.all().filter(visibility='PRIVATE', author__user__username=currentUser)
            #query set for friends
            #first get only your own 'friends' posts
            friendsQuerySet = Post.objects.filter(visibility='FRIENDS', author__user__username=currentUser)
            #next get all your friends 'friends' posts
            for friend in authorFriends:
                friendsQuerySet = friendsQuerySet | Post.objects.all().filter(visibility='FRIENDS', author__id=friend.author_id)
            #query set for friends of friends
            # friendsOfFriendsQuerySet = Post.objects.all().filter(visibility='FOAF')
            #query set for server only friends
            #first get the current user server only posts
            serverOnlyQuerySet = Post.objects.all().filter(visibility='SERVERONLY', author__user__username=currentUser)
            #next get the current user's friends that are on this server posts
            for friend in authorFriends:
                if friend.host in Site.objects.get_current().domain:
                    serverOnlyQuerySet = serverOnlyQuerySet | Post.objects.all().filter(visibility='SERVERONLY', author__id=friend.author_id)

            return publicQuerySet | privateQuerySet | friendsQuerySet | serverOnlyQuerySet

        else:
            return Post.objects.all().filter(visibility='PUBLIC')

    def list(self, request):
        queryset = self.get_queryset()
        serializer = AuthorPostSerializer(queryset,many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AuthorPostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


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
        author (object) - the author that wrote the comment
              * id - the author id
              * host - the host url of the author
              * url - the url of the author
              * displayName - the display name of the author
              * the github of the author
        comment (string) - the text of the comment
        contentType - the content type of the comment

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
        currentUser = self.request.user.username
        requester = Author.objects.get(user__username=currentUser)

        # Assume local author, and thus local friend
        if (authorHost == friendHost):

            # Get Requester
            author = Author.objects.get(id=request.data['author']['id'])

            # may need this?
            # if requester != author:
            #     return Response('Invalid', status=status.HTTP_400_BAD_REQUEST)

            # Get Requested
            friend = Author.objects.get(id=request.data['friend']['id'])


            followingObj = Friend.objects.create(author_id = request.data['friend']['id'],
                                          host = friendHost,
                                          displayName = request.data['friend']['displayName'],
                                          url = request.data['friend']['url'])

            #API specs doesn't require URL on the author side so if the url is empty in the request generate it
            if 'url' in request.data['author']:
                pendingObjURL = request.data['author']['url']
            else:
                pendingObjURL = Site.objects.get_current().domain + '/author/' + request.data['author']['id']

            pendingObj = Friend.objects.create(author_id = request.data['author']['id'],
                                          host = authorHost,
                                          displayName = request.data['author']['displayName'],
                                          url = pendingObjURL)


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
                                               displayName = request.data['author']['displayName'],
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
        authorHost = request.data['author']['host']
        friendHost = request.data['friend']['host']

        author = Author.objects.get(id=request.data['author']['id'])

        #API specs doesn't require URL on the author side so if the url is empty in the request generate it
        if 'url' in request.data['author']:
            followingObjURL = request.data['author']['url']
        else:
            followingObjURL = Site.objects.get_current().domain + '/author/' + request.data['author']['id']

        followingObj = Friend.objects.create(author_id = request.data['friend']['id'],
                                          host = friendHost,
                                          displayName = request.data['friend']['displayName'],
                                          url = followingObjURL)

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


# /api/author/author-id/friendrequests
class AuthorFriendRequests(APIView):
    """
    Endpoint: /api/author/<authorid>/friendrequests/
    Available Methods: GET
    Gets all the current friend requests from other authors that want to be your friend.
    The author will have to approve these authors to be friends.

    GET Response properties:
        id - the author id
        friendrequests - the list of friends requests the author has
    """

    def get(self,request,pk,format=None):
        queryset = Author.objects.filter(id=pk)
        serializer = ViewFriendRequestsSerializer(queryset,many=True)
        return Response(serializer.data)

# /api/author/author-id/following
class AuthorFollowing(APIView):
    """
    Endpoint: /api/author/<authorid>/following/
    Available Methods: GET
    Gets all the authors that the you are following (that you send a friend request to).
    You are awaiting a for them to accept your friend request.

    GET Response properties:
        id - the author id
        following - the list authors that you are following(that you sent a friend request to)
    """

    def get(self,request,pk,format=None):
        queryset = Author.objects.filter(id=pk)
        serializer = ViewFollowingSerializer(queryset,many=True)
        return Response(serializer.data)


# /api/friends/acceptfriend/
class AcceptFriendViewSet(APIView):

    """
    Endpoint: /api/author/friends/acceptfriend/
    Available Methods: POST

    Accepts a friend request for the currently authenticated author

    POST Request properties:
        friend - the author id of the friend you want to befriend.
                 the friend should have already sent a request to the
                 currently authenticated user.

    POST Response properties:
       No JSON is returned. If the id posted is valid, the friend will
       be removed from the currently authenticated author's pending
       friends attribute, and added to their friends attribute. A success
       message is returned alongside an HTTP 200 OK. If the ID is invalid,
       no database changes are made, and an error message is returned
       alongside an HTTP 400 OK response.
    """

    #POST:
    # { friend: <author_id> }

    def post(self, request, format=None):
        # Get Author
        currentUser = request.user
        author = Author.objects.all().filter(user = currentUser)
        author = author[0]

        friendID = request.data['friend']

        # Get friend
        for friend in author.pendingFriends.all():
            if str(friend.author_id) == str(friendID):
                friendObj = Friend.objects.create(
                                author_id=friend.author_id,
                                host=friend.host,
                                displayName=friend.displayName,
                                url=friend.url)

                if friend.host == author.host:
                    # modify friend too

                    theNewlyFriended = Author.objects.all().filter(id = friendID)
                    theNewlyFriended = theNewlyFriended[0]

                     # friend object of author
                    authObj = Friend.objects.all().filter(author_id = author.id)
                    authObj = authObj[0]

                    authorFriendObj = Friend.objects.create(author_id = authObj.author_id,
                                                      host = authObj.host,
                                                      displayName = authObj.displayName,
                                                      url = authObj.url)

                    theNewlyFriended.following.all().filter(author_id = author.id).delete()
                    theNewlyFriended.friends.add(authorFriendObj)

                author.pendingFriends.all().filter(author_id=friendID).delete()
                author.friends.add(friendObj)
                return  Response('Success', status=status.HTTP_200_OK)

        return  Response('Friend Not Found', status=status.HTTP_400_BAD_REQUEST)

# /api/friends/removefriend/
class RemoveFriendViewSet(APIView):
    """
    Endpoint: /api/author/friends/removefriend/
    Available Methods: POST

    Removes a friend attached to the currently authenticated author

    POST Request properties:
        friend - the author id of the friend you want to un-befriend.
                 the friend should already have been accepted by the
                 currently authenticated user.

    POST Response properties:
       No JSON is returned. If the id posted is valid, the friend will
       be removed from the currently authenticated author's friends attribute.
       A success message is returned alongside an HTTP 200 OK. If the ID
       is invalid, no database changes are made, and an error message is
       returned alongside an HTTP 400 BAD REQUEST response.
    """

    # POST:
    # { friend: <author_id> }

    def post(self, request, format=None):
        # Get Author
        currentUser = request.user
        author = Author.objects.all().filter(user = currentUser)
        author = author[0]

        friendID = request.data['friend']
        toDelete = None

        # Get friend
        for friend in author.friends.all():
            if str(friend.author_id) == str(friendID):

                if friend.host == author.host:
                    # symetrically remove
                    theUnfriended = Author.objects.all().filter(id = friendID)
                    theUnfriended = theUnfriended[0]
                    theUnfriended.friends.all().filter(author_id = author.id).delete()

                author.friends.all().filter(author_id=friendID).delete()
                return  Response('Success', status=status.HTTP_200_OK)

        return  Response('Friend Not Found', status=status.HTTP_400_BAD_REQUEST)

# view for /api/friends/unfollow/
class UnfollowFriendViewSet(APIView):
    """
    Endpoint: /api/author/friends/unfollow/
    Available Methods: POST

    Unfollows a given friend, essentially dropping the friend request
    the currently authenticated author sent.

    POST Request properties:
        friend - the author id of the friend you want to unfollow.
                 the currently authenticated user should have already
                 sent a friend request to the friend

    POST Response properties:
       No JSON is returned. If the id posted is valid, the friend will
       be removed from the currently authenticated author's following
       attribute. A success message is returned alongside an HTTP 200 OK.
       If the ID is invalid, no database changes are made, and an error
       message is returned alongside an HTTP 400 BAD REQUEST response.
    """
    # Post:
    # {friend: <author_id> }

    def post(self, request, format=None):
        # Get Author
        currentUser = request.user
        author = Author.objects.all().filter(user = currentUser)
        author = author[0]

        friendID = request.data['friend']

        # Get friend
        for friend in author.following.all():
            if str(friend.author_id == str(friendID)):
                # found it

                # theUnfollowed = Author.objects.all().filter(author_id = friendID)
                # theUnfollowed = theUnfollowed[0]
                # if theUnfollowed.host == author.host:
                #     #locally remove
                #     theUnfollowed.pendingFriends.objects.all().filter(author_id = author.id).delete()

                author.following.all().filter(author_id=friendID).delete()
                return  Response('Success', status=status.HTTP_200_OK)
        return  Response('Friend Not Found', status=status.HTTP_400_BAD_REQUEST)
