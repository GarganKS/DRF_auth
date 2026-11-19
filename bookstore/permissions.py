from rest_framework.permissions import SAFE_METHODS, BasePermission


class P1Permission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        email = request.user.email.lower()

        if "@" not in email:
            return False

        domain = email.rsplit("@", 1)[1]

        return domain.endswith(".edu.ua")

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return self.has_permission(request, view)
