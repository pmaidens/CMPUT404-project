from rest_framework import pagination
from rest_framework.response import Response

class PostsPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'size'

    def get_page_size(self, request):
        self.page_size = 50
        if self.page_size_query_param:
            try:
                self.page_size = pagination._positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_paginated_response(self, data):
        if self.get_previous_link() == None and self.get_next_link() == None:
            return Response({
                'query': 'posts',
                'count': self.page.paginator.count,
                'size': self.page_size,
                'posts': data
            })
        elif self.get_previous_link() == None:
            return Response({
                'query': 'posts',
                'count': self.page.paginator.count,
                'size': self.page_size,
                'next': self.get_next_link(),
                'posts': data
            })
        elif self.get_next_link() == None:
            return Response({
                'query': 'posts',
                'count': self.page.paginator.count,
                'size': self.page_size,
                'previous': self.get_previous_link(),
                'posts': data
            })
        else:
            return Response({
                'query': 'posts',
                'count': self.page.paginator.count,
                'size': self.page_size,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'posts': data
            })


class CommentsPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'size'

    def get_page_size(self, request):
        self.page_size = 50
        if self.page_size_query_param:
            try:
                self.page_size = pagination._positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_paginated_response(self, data):
        if self.get_previous_link() == None and self.get_next_link() == None:
            return Response({
                'query': 'comments',
                'count': self.page.paginator.count,
                'size': self.page_size,
                'comments': data
            })
        elif self.get_previous_link() == None:
            return Response({
                'query': 'comments',
                'count': self.page.paginator.count,
                'size': self.page_size,
                'next': self.get_next_link(),
                'comments': data
            })
        elif self.get_next_link() == None:
            return Response({
                'query': 'comments',
                'count': self.page.paginator.count,
                'size': self.page_size,
                'previous': self.get_previous_link(),
                'comments': data
            })
        else:
            return Response({
                'query': 'comments',
                'count': self.page.paginator.count,
                'size': self.page_size,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'comments': data
            })
