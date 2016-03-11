from rest_framework import generics
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .serializers import *
import uuid
from rest_framework.permissions import  AllowAny
from rest_framework.decorators import detail_route


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




#class FriendDetailViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,viewsets.GenericViewSets):
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


    @detail_route(methods=['post','get'])
    def test(self, request, **kwargs):

        author = self.get_object()

        self.queryset = self.get_queryset()
        self.serializer_class = FriendDetailSerializer

        if request.method == 'POST':

            # request.data is from the POST object. We want to take these
            # values and supplement it with the user.id that's defined
            # in our URL parameter
            data = {
                'query': request.data['query'],
                'author': request.data['author'],
                'authors': request.data['authors'],
            }

            serializer = test(data=data,partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Return GET by default
        else:

            serializer = FriendDetailSerializer(instance=self.queryset, many=True)

            return Response(serializer.data)

#
# class FriendRequestViewSet(viewsets.ModelViewSet):
#
#     queryset = Post.objects.all()
#     serializer_class = PostsSerializer
