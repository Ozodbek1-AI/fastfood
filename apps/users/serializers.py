# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken
#
# User = get_user_model()
#
#
# # REGISTER serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User.objects.create(username=validated_data['username'])
#         user.set_password(password)
#         user.save()
#         return user
#
#
# # LOGIN serializer
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#
#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')
#
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if not user:
#                 raise serializers.ValidationError("Username yoki password noto‘g‘ri")
#             if not user.is_active:
#                 raise serializers.ValidationError("Foydalanuvchi aktiv emas")
#         else:
#             raise serializers.ValidationError("Username va password kiriting")
#
#         attrs['user'] = user
#         return attrs
#
#
#
#
# # UPDATE serializer
# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'phone', 'email', 'first_name', 'last_name']
#         extra_kwargs = {
#             'username': {'required': True},
#             'phone': {'required': False},
#             'email': {'required': False},
#             'first_name': {'required': False},
#             'last_name': {'required': False},
#         }
#
#     def validate_username(self, value):
#         user = self.instance
#         if User.objects.exclude(pk=user.pk).filter(username=value).exists():
#             raise serializers.ValidationError("Bu username allaqachon mavjud")
#         return value
#
#     def validate_email(self, value):
#         user = self.instance
#         if value and User.objects.exclude(pk=user.pk).filter(email=value).exists():
#             raise serializers.ValidationError("Bu email allaqachon mavjud")
#         return value
#
#     def validate_phone(self, value):
#         user = self.instance
#         if value and User.objects.exclude(pk=user.pk).filter(phone=value).exists():
#             raise serializers.ValidationError("Bu phone allaqachon mavjud")
#         return value
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'phone', 'email', 'first_name', 'last_name']
#
#

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


# REGISTER
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(username=validated_data['username'])
        user.set_password(password)
        user.save()
        return user


# LOGIN
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        username = attrs.get('username')
        password = attrs.get('password')
        if not username or not password:
            raise serializers.ValidationError("Username va password kiriting")
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Username yoki password noto‘g‘ri")
        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi aktiv emas")
        attrs['user'] = user
        return attrs


# UPDATE USER
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'phone', 'email', 'first_name', 'last_name', 'password']

    def validate_username(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Bu username allaqachon mavjud")
        return value

    def validate_email(self, value):
        user = self.instance
        if value and User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Bu email allaqachon mavjud")
        return value

    def validate_phone(self, value):
        user = self.instance
        if value and User.objects.exclude(pk=user.pk).filter(phone=value).exists():
            raise serializers.ValidationError("Bu phone allaqachon mavjud")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# USER PROFILE
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', 'first_name', 'last_name', 'is_active']
