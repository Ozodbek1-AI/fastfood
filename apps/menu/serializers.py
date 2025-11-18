from rest_framework import serializers
from .models import MenuItem

# ======================
# Create serializer
# ======================
class MenuItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'restaurant', 'title', 'description', 'price', 'measurement_type', 'is_active']

    def validate_restaurant(self, value):
        """
        Faqat restoran egasi item qo‘shishi mumkin.
        """
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("You can only add items to your own restaurant.")
        return value


# ======================
# Update serializer
# ======================
class MenuItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title', 'description', 'price', 'measurement_type', 'is_active']

    def validate(self, attrs):
        """
        Faqat restaurant egasi itemni update qilishi mumkin.
        """
        item = self.instance
        user = self.context['request'].user
        if item.restaurant.owner != user:
            raise serializers.ValidationError("You can only update items of your own restaurant.")
        return attrs


# ======================
# List serializer
# ======================
class MenuItemListSerializer(serializers.ModelSerializer):
    restaurant = serializers.StringRelatedField(read_only=True)  # restaurant nomini ko‘rsatadi

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'title',
            'description',
            'price',
            'measurement_type',
            'is_active',
            'restaurant',
            'created_at',
            'updated_at',
        ]


# ======================
# Delete serializer
# ======================
class MenuItemDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id']
        read_only_fields = ['id']  # delete uchun faqat id kerak, o‘zgartirish mumkin emas
