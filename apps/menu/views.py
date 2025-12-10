from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, AllowAny
from .models import MenuItem
from .serializers import (
    MenuItemCreateSerializer,
    MenuItemUpdateSerializer,
    MenuItemListSerializer,
    MenuItemDeleteSerializer
)


# ======================
# Create MenuItem
# ======================
class MenuItemCreateAPIView(CreateAPIView):
    serializer_class = MenuItemCreateSerializer
    permission_classes = [AllowAny]


    def perform_create(self, serializer):
        restaurant = serializer.validated_data.get('restaurant')
        user = self.request.user
        if restaurant.owner != user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only add items to your own restaurant.")
        serializer.save()


# ======================
# Update MenuItem (PATCH)
# ======================
class MenuItemUpdateAPIView(UpdateAPIView):
    serializer_class = MenuItemUpdateSerializer
    permission_classes = [AllowAny]
    queryset = MenuItem.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        return MenuItem.objects.filter(restaurant__owner=self.request.user)


# ======================
# Delete MenuItem (DELETE)
# ======================
class MenuItemDeleteAPIView(DestroyAPIView):
    serializer_class = MenuItemDeleteSerializer
    permission_classes = [AllowAny]
    queryset = MenuItem.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        return MenuItem.objects.filter(restaurant__owner=self.request.user)


# ======================
# List MenuItems (GET)
# ======================
class MenuItemListAPIView(ListAPIView):
    serializer_class = MenuItemListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return MenuItem.objects.filter(restaurant__owner=self.request.user)