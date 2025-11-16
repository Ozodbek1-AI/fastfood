from django.urls import path
from .views import (
    OrderCreateAPIView,
    OrderListAPIView,
    OrderDetailAPIView,
    OrderUpdateAPIView,
    OrderDeleteAPIView,
)

urlpatterns = [
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('list/', OrderListAPIView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('update/<int:pk>/', OrderUpdateAPIView.as_view(), name='order-update'),
    path('delete/<int:pk>/', OrderDeleteAPIView.as_view(), name='order-delete'),
]
