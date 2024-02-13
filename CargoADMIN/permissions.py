# Permission Class: IsLoggedInAndPasswordSet
# کلاس مجوز: IsLoggedInAndPasswordSet

from rest_framework import permissions


class IsLoggedInAndIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is logged in
        # بررسی اینکه کاربر لاگین کرده
        if not request.user.is_authenticated:
            return False
        if request.user.profile.user_type == 'ادمین':
            return True
        else:
            return False
