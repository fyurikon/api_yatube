from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class OnlyAuthorCanModify(IsAuthenticated):
    """Only author can modify. Others read only."""
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
