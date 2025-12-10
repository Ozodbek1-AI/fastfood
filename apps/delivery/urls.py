from django.urls import path
from .views import (
    CourierRegistrationView,
    CourierProfileViewSet,
    DeliveryViewSet,
)

urlpatterns = [
    path('register/', CourierRegistrationView.as_view(), name='register'),

    # Courier Profile
    path('profile/', CourierProfileViewSet.as_view({'get': 'me'}), name='profile'),
    path('profile/update/', CourierProfileViewSet.as_view({'patch': 'update'}), name='profile-update'),
    path('profile/status/', CourierProfileViewSet.as_view({'patch': 'update_status'}), name='profile-status'),
    path('profile/statistics/', CourierProfileViewSet.as_view({'get': 'statistics'}), name='statistics'),

    # Deliveries
    path('orders/available/', DeliveryViewSet.as_view({'get': 'available'}), name='available-orders'),
    path('orders/my/', DeliveryViewSet.as_view({'get': 'my_deliveries'}), name='my-orders'),
    path('orders/completed/', DeliveryViewSet.as_view({'get': 'completed'}), name='completed-orders'),
    path('orders/<int:pk>/', DeliveryViewSet.as_view({'get': 'retrieve'}), name='order-detail'),
    path('orders/<int:pk>/accept/', DeliveryViewSet.as_view({'post': 'accept'}), name='order-accept'),
    path('orders/<int:pk>/status/', DeliveryViewSet.as_view({'post': 'update_status'}), name='order-status'),
    path('orders/<int:pk>/cancel/', DeliveryViewSet.as_view({'post': 'cancel'}), name='order-cancel'),
]