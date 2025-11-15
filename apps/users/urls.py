# from django.urls import path
# from .views import RegisterAPIView, LoginAPIView, UserUpdateAPIView, UserProfileAPIView, UserDeleteAPIView
#
# urlpatterns = [
#     path('register/', RegisterAPIView.as_view()),
#     path('login/', LoginAPIView.as_view()),
#     path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
#     path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user-delete'),
#     path('profile/<int:pk>/', UserProfileAPIView.as_view(), name='user-profile'),
# ]
from django.urls import path
from .views import (
    RegisterAPIView, LoginAPIView, UserUpdateAPIView,
    UserDeleteAPIView, UserProfileByIdAPIView, UserListAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('profile/<int:pk>/', UserProfileByIdAPIView.as_view(), name='user-profile-by-id'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
]
