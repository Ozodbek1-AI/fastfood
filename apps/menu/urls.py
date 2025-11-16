from django.urls import path
from .views import (
    MenuItemListAPIView,
    MenuItemDetailAPIView,
    MenuItemCreateAPIView,
    MenuItemUpdateAPIView,
    MenuItemDeleteAPIView
)

urlpatterns = [
    path('menu/', MenuItemListAPIView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', MenuItemDetailAPIView.as_view(), name='menu-detail'),
    path('menu/create/', MenuItemCreateAPIView.as_view(), name='menu-create'),
    path('menu/<int:pk>/update/', MenuItemUpdateAPIView.as_view(), name='menu-update'),
    path('menu/<int:pk>/delete/', MenuItemDeleteAPIView.as_view(), name='menu-delete'),
]
