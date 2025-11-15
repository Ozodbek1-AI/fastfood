from rest_framework.permissions import BasePermission

class IsAdminOrSelf(BasePermission):
    """
    Foydalanuvchi faqat o'zini update/delete qilishi mumkin,
    admin esa barcha foydalanuvchilarni boshqara oladi
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
