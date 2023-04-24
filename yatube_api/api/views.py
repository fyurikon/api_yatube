from django.shortcuts import get_object_or_404
from posts.models import Group, Post
from rest_framework import viewsets
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)

from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class OnlyAuthorCanModify(BasePermission):
    """Only author can modify. Others read only."""
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """Post viewset."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, OnlyAuthorCanModify)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Comment viewset."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, OnlyAuthorCanModify)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Group viewset."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
