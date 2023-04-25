from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from .permissions import OnlyAuthorCanModify


class PostViewSet(viewsets.ModelViewSet):
    """Post viewset."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OnlyAuthorCanModify,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Comment viewset."""
    serializer_class = CommentSerializer
    permission_classes = (OnlyAuthorCanModify,)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Group viewset."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
