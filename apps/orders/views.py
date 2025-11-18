from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderCreateSerializer, OrderListSerializer, OrderCancelSerializer


# ======================
# Create Order
# ======================
class OrderCreateAPIView(CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ======================
# List Orders
# ======================
class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# ======================
# Cancel Order
# ======================
class OrderCancelAPIView(DestroyAPIView):
    serializer_class = OrderCancelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        # Faqat o‘zi yaratgan orderni bekor qilishi mumkin
        return Order.objects.filter(user=self.request.user)
