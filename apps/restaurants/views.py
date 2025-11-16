from rest_framework.generics import (
    CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
)
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant
from .serializers import (
    RestaurantCreateSerializer,
    RestaurantUpdateSerializer,
    RestaurantListSerializer,
    RestaurantDeleteSerializer
)

# ======================
# Create restaurant
# ======================
class RestaurantCreateAPIView(CreateAPIView):
    serializer_class = RestaurantCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# ======================
# Update restaurant (PATCH)
# ======================
class RestaurantUpdateAPIView(UpdateAPIView):
    serializer_class = RestaurantUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        # Faqat restaurant egasi update qila oladi
        return Restaurant.objects.filter(owner=self.request.user)


# ======================
# Delete restaurant (DELETE)
# ======================
class RestaurantDeleteAPIView(DestroyAPIView):
    serializer_class = RestaurantDeleteSerializer
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        # Faqat restaurant egasi o‘chira oladi
        return Restaurant.objects.filter(owner=self.request.user)


# ======================
# List restaurants (GET)
# ======================
class RestaurantListAPIView(ListAPIView):
    serializer_class = RestaurantListSerializer
    permission_classes = [IsAuthenticated]
    queryset = Restaurant.objects.all()
