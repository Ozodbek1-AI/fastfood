from django.urls import path
from .views import OrderCreateAPIView, OrderCancelAPIView, OrderListAPIView

urlpatterns = [
    path('create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('my/', OrderListAPIView.as_view(), name='order-my'),
    path('cancel/<int:pk>/', OrderCancelAPIView.as_view(), name='order-cancel'),
]
