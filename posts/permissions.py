from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post to edit or delete it.
    """
    def has_permission(self, request, view):
        # Allow any read-only request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # For write operations, user must be authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of the post.
        return obj.author == request.user
