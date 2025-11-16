from rest_framework import serializers
from .models import Order
from apps.menu.models import MenuItem


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('menu_item', 'quantity')

    def validate(self, attrs):
        menu_item = attrs.get('menu_item')

        if not MenuItem.objects.filter(id=menu_item.id, is_active=True).exists():
            raise serializers.ValidationError("Bu menu item hozir mavjud emas.")

        if attrs['quantity'] < 1:
            raise serializers.ValidationError("Quantity 1 dan kichik bo‘la olmaydi.")

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderListSerializer(serializers.ModelSerializer):
    menu_item_title = serializers.CharField(source='menu_item.title', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'menu_item_title', 'quantity', 'status', 'created_at')


class OrderDetailSerializer(serializers.ModelSerializer):
    menu_item_title = serializers.CharField(source='menu_item.title', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'menu_item_title', 'quantity', 'status', 'created_at')


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('quantity',)

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity 1 dan kichik bo‘lmaydi.")
        return value


class OrderDeleteSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()

    def validate_confirm(self, value):
        if value is not True:
            raise serializers.ValidationError("Delete qilish uchun confirm=True bo‘lishi kerak.")
        return value
