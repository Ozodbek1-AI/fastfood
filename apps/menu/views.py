from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem
from .serializers import (
    MenuItemCreateSerializer,
    MenuItemUpdateSerializer,
    MenuItemReadSerializer
)
from .permissions import IsAdminOrReadOnly

# List
class MenuItemListAPIView(generics.ListAPIView):
    queryset = MenuItem.objects.filter(is_active=True)
    serializer_class = MenuItemReadSerializer
    permission_classes = [IsAuthenticated]  # Hamma token bilan ko‘ra oladi

# Retrieve
class MenuItemDetailAPIView(generics.RetrieveAPIView):
    queryset = MenuItem.objects.filter(is_active=True)
    serializer_class = MenuItemReadSerializer
    permission_classes = [IsAuthenticated]  # Hamma token bilan ko‘ra oladi

# Create
class MenuItemCreateAPIView(generics.CreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

# Update
class MenuItemUpdateAPIView(generics.UpdateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

# Delete
class MenuItemDeleteAPIView(generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemReadSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()
