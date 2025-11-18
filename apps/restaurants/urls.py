from django.urls import path
from .views import (
    RestaurantCreateAPIView,
    RestaurantUpdateAPIView,
    RestaurantDeleteAPIView,
    RestaurantListAPIView
)

urlpatterns = [
    path('create/', RestaurantCreateAPIView.as_view(), name='restaurant-create'),
    path('<int:pk>/update/', RestaurantUpdateAPIView.as_view(), name='restaurant-update'),
    path('<int:pk>/delete/', RestaurantDeleteAPIView.as_view(), name='restaurant-delete'),
    path('list/', RestaurantListAPIView.as_view(), name='restaurant-list'),
]
