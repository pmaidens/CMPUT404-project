from rest_framework import viewsets
from .serializers import *

class AuthorViewSet(viewsets.ModelViewSet):

    """
    Returns a list of all authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
