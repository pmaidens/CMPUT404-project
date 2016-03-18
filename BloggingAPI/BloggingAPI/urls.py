from django.conf.urls import patterns, url, include
from rest_framework import routers
from rest_framework_nested import routers
from django.contrib import admin
from .views import *

class APIRouter(routers.DefaultRouter):

    def get_api_root_view(self):
        api_root_view = super(APIRouter, self).get_api_root_view()
        ApiRootClass = api_root_view.cls

        class MyAPIRoot(ApiRootClass):
            """
            Endpoint: /api/
            This is the api root end point and it lists the following api endpoints that are available to the user.
            Endpoint: /api/author/ gives the list of authors
            Endpoint: /api/posts/ gives the list of posts
            Endpoint: /api/posts/{AUTHOR_ID}/comments gives the list of comments of a post
            Endpoint: /api/friends/ gives the list of friends
            """
            pass

        return MyAPIRoot.as_view()

apiRouter = APIRouter()

# http://service/author (ONLY USED FOR TESTING)
# http://service/author/{AUTHOR_ID}
apiRouter.register(r'author', AuthorViewSet)

# http://service/posts
# http://service/posts/{POST_ID}
apiRouter.register(r'posts', PostsViewSet)

# http://service/author/posts
# apiRouter.register(r'author/posts', CurrentAuthorPostsViewSet)

# http://service/author/{AUTHOR_ID}/posts
#posts_router = routers.NestedSimpleRouter(apiRouter, r'author', lookup='author')
#posts_router.register(r'posts', AuthorPostsViewSet)

# http://service/posts/{post_id}/comments
comments_router = routers.NestedSimpleRouter(apiRouter, r'posts', lookup='posts')
comments_router.register(r'comments', PostCommentsViewSet, base_name='comments')

# http://service/friends/<authorid>
#apiRouter.register(r'friends', FriendDetailViewSet,'friends')


urlpatterns = [
    # Examples:
    # url(r'^$', 'BloggingAPI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/', include(apiRouter.urls)),
    # url(r'^', include(posts_router.urls)),
    url(r'^api/', include(comments_router.urls)),
    url(r'^api/friends/(?P<pk>[^/.]+)/$', FriendDetailView.as_view()),
    url(r'^api/friends/$', FriendOverviewView.as_view()),
    url(r'^api/author/(?P<pk>[^/.]+)/posts/$', AuthorSpecificPosts.as_view()),
    url(r'^api/friendrequest/$',FriendRequestViewSet.as_view()),
]

#url(r'^test/(?P<pk>[\d]+)/$', FriendPostViewSet.as_view(), name='test-list'),
#url(r'^test/(?P<pk>[\d]+)/$', testInstanceView.as_view(), name='test-instance'
