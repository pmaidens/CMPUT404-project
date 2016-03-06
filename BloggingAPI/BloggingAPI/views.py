from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .serializers import *

class AuthorViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    # def create(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #
    #     if serializer.is_valid():
    #         Author.create_Author(**serializer.validated_data)
    #         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    #
    #     print serializer.errors
    #     return Response({'message': 'Account could not be created with received data.'}, status=status.HTTP_400_BAD_REQUEST)


class PostsViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()

    def get_serializer_class(self):
        serializer_class = ViewPostsSerializer
        if self.request.method == 'POST':
            serializer_class = UpdatePostsSerializer
        elif self.request.method == 'PUT':
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

# class FriendsViewSet(viewsets.ModelViewSet):
#
#     queryset = Post.objects.all()
#     serializer_class = PostsSerializer
#
#
# class FriendRequestViewSet(viewsets.ModelViewSet):
#
#     queryset = Post.objects.all()
#     serializer_class = PostsSerializer
