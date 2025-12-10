# permissions.py
from rest_framework import permissions


class IsCourier(permissions.BasePermission):
    """Faqat courier foydalanuvchilar uchun"""
    message = "Siz courier emassiz"

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                hasattr(request.user, 'courier_profile')
        )


class IsCourierOwner(permissions.BasePermission):
    """Faqat o'z profilini tahrirlash mumkin"""
    message = "Siz faqat o'z profilingizni tahrirlashingiz mumkin"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsApprovedCourier(permissions.BasePermission):
    """Faqat tasdiqlangan courierlar"""
    message = "Sizning profilingiz hali tasdiqlanmagan"

    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                hasattr(request.user, 'courier_profile') and
                request.user.courier_profile.status == 'approved' and
                request.user.courier_profile.is_active
        )


class IsDeliveryCourier(permissions.BasePermission):
    """Faqat buyurtmani olib ketgan courier tahrirlashi mumkin"""
    message = "Bu yetkazib berish sizga tegishli emas"

    def has_object_permission(self, request, view, obj):
        return obj.courier == request.user
