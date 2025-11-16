from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView,
    UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import (
    OrderCreateSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    OrderUpdateSerializer,
    OrderDeleteSerializer
)
from .permissions import IsOwnerOrAdmin


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]


class OrderListAPIView(ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class OrderUpdateAPIView(UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]


class OrderDeleteAPIView(DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDeleteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
