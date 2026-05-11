from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    """Generic role-based permission.

    Views can set `required_roles = ['super_admin', 'executive']` to restrict access.
    If `required_roles` is not set on the view, this permission allows access.
    """

    def has_permission(self, request, view):
        required = getattr(view, 'required_roles', None)
        if required is None:
            return True

        user = getattr(request, 'user', None)
        if not user or not getattr(user, 'is_authenticated', False):
            return False

        return user.role in required
