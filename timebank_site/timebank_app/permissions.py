from rest_framework.permissions import SAFE_METHODS, BasePermission


class SafeMethodsOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj=None):
        return request.method in SAFE_METHODS


class AdminOrAuthorCanEdit(BasePermission):

    def has_object_permission(self, request, view, obj=None):
        """Only the author can modify existing instances."""
        is_safe = request.method in SAFE_METHODS

        try:
            is_author = request.user == obj.author
        except AttributeError:
            is_author = False

        if is_safe or is_author or request.user.is_superuser:
            print("has_object_permission Request passed")
        else:
            print("has_object_permission Request failed")
        return is_safe or is_author or request.user.is_superuser
