from django.urls import path
from .views import (
    MenuItemCreateAPIView,
    MenuItemUpdateAPIView,
    MenuItemDeleteAPIView,
    MenuItemListAPIView
)

urlpatterns = [
    # Create menu item
    path('create/', MenuItemCreateAPIView.as_view(), name='menuitem-create'),

    # Update menu item (PATCH)
    path('<int:pk>/update/', MenuItemUpdateAPIView.as_view(), name='menuitem-update'),

    # Delete menu item (DELETE)
    path('<int:pk>/delete/', MenuItemDeleteAPIView.as_view(), name='menuitem-delete'),

    # List menu items (GET)
    path('list/', MenuItemListAPIView.as_view(), name='menuitem-list'),
]
