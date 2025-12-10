from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CourierProfile, Delivery, DeliveryHistory
from apps.orders.serializers import OrderSerializer

User = get_user_model()


class CourierRegistrationSerializer(serializers.ModelSerializer):
    """Courier ro'yxatdan o'tish uchun"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    full_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    passport_number = serializers.CharField(max_length=30)
    transport_type = serializers.ChoiceField(choices=CourierProfile.TRANSPORT_TYPES)
    transport_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm',
                  'full_name', 'phone_number', 'passport_number',
                  'transport_type', 'transport_number']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Parollar mos kelmaydi")
        return data

    def create(self, validated_data):
        # Courier profil uchun ma'lumotlar
        full_name = validated_data.pop('full_name')
        phone_number = validated_data.pop('phone_number')
        passport_number = validated_data.pop('passport_number')
        transport_type = validated_data.pop('transport_type')
        transport_number = validated_data.pop('transport_number', '')
        validated_data.pop('password_confirm')

        # User yaratish
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        # Courier profil yaratish
        CourierProfile.objects.create(
            user=user,
            full_name=full_name,
            phone_number=phone_number,
            passport_number=passport_number,
            transport_type=transport_type,
            transport_number=transport_number,
            status='pending'
        )

        return user


class CourierProfileSerializer(serializers.ModelSerializer):
    """Courier profil ma'lumotlari"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    total_deliveries = serializers.SerializerMethodField()
    completed_today = serializers.SerializerMethodField()

    class Meta:
        model = CourierProfile
        fields = [
            'id', 'username', 'email', 'full_name', 'phone_number',
            'passport_number', 'transport_type', 'transport_number',
            'status', 'is_active', 'is_online', 'total_deliveries',
            'completed_today', 'created_at', 'approved_at'
        ]
        read_only_fields = ['id', 'status', 'is_active', 'created_at', 'approved_at']

    def get_total_deliveries(self, obj):
        return obj.total_deliveries()

    def get_completed_today(self, obj):
        return obj.completed_today()


class CourierStatusUpdateSerializer(serializers.ModelSerializer):
    """Courier online/offline qilish uchun"""

    class Meta:
        model = CourierProfile
        fields = ['is_online']


class DeliveryHistorySerializer(serializers.ModelSerializer):
    """Yetkazib berish tarixi"""

    class Meta:
        model = DeliveryHistory
        fields = ['id', 'status', 'note', 'latitude', 'longitude', 'created_at']


class DeliveryListSerializer(serializers.ModelSerializer):
    """Courier uchun orderlar ro'yxati"""
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    customer_name = serializers.CharField(source='order.user.get_full_name', read_only=True)
    total_amount = serializers.DecimalField(source='order.total_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'id', 'order_number', 'customer_name', 'customer_phone',
            'delivery_address', 'delivery_fee', 'total_amount', 'status',
            'created_at', 'estimated_delivery_time'
        ]


class DeliveryDetailSerializer(serializers.ModelSerializer):
    """Buyurtma to'liq ma'lumotlari"""
    order = OrderSerializer(read_only=True)
    courier_name = serializers.CharField(source='courier.get_full_name', read_only=True)
    history = DeliveryHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Delivery
        fields = [
            'id', 'order', 'courier', 'courier_name', 'status',
            'delivery_fee', 'delivery_address', 'delivery_notes',
            'customer_phone', 'latitude', 'longitude',
            'created_at', 'assigned_at', 'picked_up_at', 'delivered_at',
            'estimated_delivery_time', 'actual_delivery_time', 'history'
        ]


class DeliveryStatusUpdateSerializer(serializers.ModelSerializer):
    """Yetkazib berish statusini yangilash"""
    note = serializers.CharField(required=False, allow_blank=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)

    class Meta:
        model = Delivery
        fields = ['status', 'note', 'latitude', 'longitude']

    def update(self, instance, validated_data):
        note = validated_data.pop('note', '')
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)

        # Status yangilash
        instance = super().update(instance, validated_data)

        # Tarixga qo'shish
        DeliveryHistory.objects.create(
            delivery=instance,
            status=instance.status,
            note=note,
            latitude=latitude,
            longitude=longitude
        )

        return instance


class CourierStatsSerializer(serializers.Serializer):
    """Courier statistikasi"""
    total_deliveries = serializers.IntegerField()
    completed_today = serializers.IntegerField()
    completed_this_week = serializers.IntegerField()
    completed_this_month = serializers.IntegerField()
    total_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    average_delivery_time = serializers.DurationField()
    success_rate = serializers.FloatField()