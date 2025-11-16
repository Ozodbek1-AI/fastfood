from django.urls import path
from .views import (
    RestaurantCreateAPIView,
    RestaurantUpdateAPIView,
    RestaurantDeleteAPIView,
    RestaurantListAPIView
)

urlpatterns = [
    # Create restaurant
    path('create/', RestaurantCreateAPIView.as_view(), name='restaurant-create'),

    # Update restaurant (PATCH)
    path('<int:pk>/update/', RestaurantUpdateAPIView.as_view(), name='restaurant-update'),

    # Delete restaurant (DELETE)
    path('<int:pk>/delete/', RestaurantDeleteAPIView.as_view(), name='restaurant-delete'),

    # List restaurants (GET)
    path('list/', RestaurantListAPIView.as_view(), name='restaurant-list'),
]
