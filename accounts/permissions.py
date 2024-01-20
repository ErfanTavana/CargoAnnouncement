from rest_framework import permissions
from .models import PasswordSetStatus

class IsLoggedInAndPasswordSet(permissions.BasePermission):
    def has_permission(self, request, view):
        # بررسی اینکه کاربر لاگین کرده
        if not request.user.is_authenticated:
            return False

        # بررسی اینکه کاربر پسورد خود را تنظیم کرده
        try:
            password_set_status = PasswordSetStatus.objects.get(token=request.auth)
            return password_set_status.is_password_set
        except PasswordSetStatus.DoesNotExist:
            return False