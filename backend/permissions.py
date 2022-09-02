from rest_framework import permissions


class OnlyShops(permissions.BasePermission):

    edit_methods = ("PUT", "GET", "POST",)
    message = 'Error: Только для магазинов'

    def has_permission(self, request, view):
        if request.user.type == 'shop':
            return True
        return False
