from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperuser(BasePermission):
    message = "Пользователь должен быть суперадмином"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOrder(BasePermission):
    courier_method = ("PUT", "PATCH", "GET")
    admin_method = ("GET", "PUT", "PATCH", "DELETE")
    client_method = "DELETE"
    anonymous_method = ("GET", "POST")

    def has_permission(self, request, view):
        return bool(
            request.user.is_anonymous
            or request.user.role == "Клиент"
            and request.method not in self.client_method
            or request.user.role == "Админ"
            and request.method in self.admin_method
            or request.user.role == "Курьер"
            and request.method in self.courier_method
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous or request.user.role == "Админ" and request.method in self.admin_method:
            return True
        if request.user.role == "Курьер" and request.method in self.courier_method:
            return True
        if request.user.role == 'Клиент' or request.user.is_anonymous and request.method not in self.client_method:
            return True
        return False


class IsAdminOrReadOnly(BasePermission):
    """
    Allows access only to admin or give a read only request
    """
    message = "Пользователь должен быть админом"

    def has_permission(self, request, view):
        if (
            request.method in SAFE_METHODS
            or request.user.is_anonymous
            or request.user.role == "Админ"
        ):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == "Админ":
            return True
        if request.user.is_anonymous and request.method in SAFE_METHODS:
            return True
        return False


class IsCourierOrReadOnly(BasePermission):
    message = "Пользователь должен быть курьером"

    def has_permission(self, request, view):
        if (
            request.method in SAFE_METHODS
            or request.user.is_anonymous
            or request.user.role == "Курьер"
        ):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == "Курьер":
            return True
        if request.user.is_anonymous and request.method in SAFE_METHODS:
            return True
        return False


class IsClientOrReadOnly(BasePermission):
    message = "Пользователь должен быть курьером"

    def has_permission(self, request, view):
        if (
            request.method in SAFE_METHODS
            or request.user.is_anonymous
            or request.user.role == "Клиент"
        ):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == "Клиент":
            return True
        if request.user.is_anonymous and request.method in SAFE_METHODS:
            return True
        return False


class IsFloristOrReadOnly(BasePermission):
    """
    Allows access only to florist or give a read only request
    """

    message = "Пользователь должен быть флористом"

    def has_permission(self, request, view):
        if (
            request.method in SAFE_METHODS
            or request.user.is_anonymous
            or request.user.role == "Флорист"
        ):
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.role == "Флорист":
            return True
        if request.user.is_anonymous and request.method in SAFE_METHODS:
            return True
        return False
