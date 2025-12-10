from rest_framework import serializers
from .models import Order, OrderItem
from apps.menu.models import MenuItem


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.filter(is_active=True))

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'price']
        read_only_fields = ['price']

    def create(self, validated_data):
        menu_item = validated_data['menu_item']
        quantity = validated_data['quantity']
        validated_data['price'] = menu_item.price * quantity
        return super().create(validated_data)


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'location', 'items', 'created_at']
        read_only_fields = ['created_at']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must have at least one item.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'location', 'items', 'created_at']


class OrderCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'