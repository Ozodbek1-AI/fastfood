# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import get_user_model
# from .serializers import RegisterSerializer, UserUpdateSerializer, LoginSerializer, UserProfileSerializer
#
# User = get_user_model()
#
#
# # REGISTER
# class RegisterAPIView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
#
#
# # LOGIN with JWT
# class LoginAPIView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'user_id': user.id,
#             'username': user.username
#         })
#
#
# # UPDATE (JWT token bilan)
# class UserUpdateAPIView(generics.UpdateAPIView):
#     serializer_class = UserUpdateSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = User.objects.all()
#
#
# # DELETE USER (by ID)
# class UserDeleteAPIView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = User.objects.all()
#
#
# # USER PROFILE
# class UserProfileAPIView(generics.RetrieveAPIView):
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = User.objects.all()

from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    RegisterSerializer, LoginSerializer, UserUpdateSerializer, UserProfileSerializer
)
from .permissions import IsAdminOrSelf

User = get_user_model()


# REGISTER
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# LOGIN
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username
        })


# UPDATE USER
class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]
    queryset = User.objects.all()


# DELETE USER (soft delete)
class UserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSelf]
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


# USER PROFILE by ID
class UserProfileByIdAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()


# LIST USERS (admin only) + search + pagination
class UserListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'email', 'phone']
    filterset_fields = ['is_active']
    pagination_class = PageNumberPagination
