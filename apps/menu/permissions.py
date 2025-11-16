from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Oddiy foydalanuvchi faqat o'qishi mumkin.
    Admin yaratish, update va delete qilishi mumkin.
    """
    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS uchun ruxsat
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # POST, PATCH, DELETE faqat admin
        return request.user and request.user.is_staff
