from django.conf.urls import patterns, url, include
from rest_framework import routers
from rest_framework_nested import routers
from django.contrib import admin
from .views import *


apiRouter = routers.DefaultRouter()

# http://service/author (ONLY USED FOR TESTING)
# http://service/author/{AUTHOR_ID}
apiRouter.register(r'author', AuthorViewSet)

# http://service/posts
# http://service/posts/{POST_ID}
apiRouter.register(r'posts', PostsViewSet)

# http://service/author/posts
# apiRouter.register(r'author/posts', CurrentAuthorPostsViewSet)

# http://service/author/{AUTHOR_ID}/posts
# posts_router = routers.NestedSimpleRouter(apiRouter, r'author', lookup='author')
# posts_router.register(r'posts', AuthorPostsViewSet)

# http://service/posts/{post_id}/comments
comments_router = routers.NestedSimpleRouter(apiRouter, r'posts', lookup='posts')
comments_router.register(r'comments', PostCommentsViewSet, base_name='comments')

# http://service/friends/<authorid>
apiRouter.register(r'friends', FriendsViewSet)

# http://service/friendrequest
# apiRouter.register(r'friendrequest', FriendRequestViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', 'BloggingAPI.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/', include(apiRouter.urls)),
    # url(r'^', include(posts_router.urls)),
    url(r'^api/', include(comments_router.urls)),
]
