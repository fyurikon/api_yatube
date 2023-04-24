from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='posts')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(r'groups', GroupViewSet, basename='groups')


urlpatterns = [
    path('', include(router.urls)),
]
