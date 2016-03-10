from rest_framework import generics
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import  *
from .serializers import *
import uuid
from .permissions import *

class AuthorViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Author.objects.all()
    # permission_classes = (AuthorPermissions,)

    def get_serializer_class(self):
        serializer_class = ViewAuthorSerializer
        if self.request.method == 'PUT':
            serializer_class = UpdateAuthorSerializer
        return serializer_class

class PostsViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Post.objects.all()
        visibility = self.request.query_params.get('visibility', None)
        if visibility is not None:
            queryset = queryset.filter(visibility=visibility)
        else:
            queryset = Post.objects.all().filter(visibility='PUBLIC')
        return queryset

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

class PostCommentsViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()

    def get_serializer_class(self):
        serializer_class = ViewCommentSerializer
        if self.request.method == 'POST':
            serializer_class = UpdateCommentSerializer
        elif self.request.method == 'PUT':
            serializer_class = UpdateCommentSerializer
        return serializer_class


class FriendDetailViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    model = Author
    serializer_class = FriendDetailSerializer

    def get_queryset(self):
        queryset = Author.objects.all()
        pks = self.request.query_params.get('pks', None)

        if pks is not None:
            queryset = queryset.filter(pks__in=pks)

        return queryset

#
# class FriendRequestViewSet(viewsets.ModelViewSet):
#
#     queryset = Post.objects.all()
#     serializer_class = PostsSerializer
