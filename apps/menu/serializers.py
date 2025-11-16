from rest_framework import serializers
from .models import MenuItem

# CREATE serializer
class MenuItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title', 'description', 'price', 'measurement_type', 'is_active']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price 0 dan katta bo‘lishi kerak")
        return value

    def validate_measurement_type(self, value):
        if value not in dict(MenuItem.MEASUREMENT_CHOICES):
            raise serializers.ValidationError("Invalid measurement type")
        return value

# UPDATE serializer
class MenuItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title', 'description', 'price', 'measurement_type', 'is_active']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price 0 dan katta bo‘lishi kerak")
        return value

    def validate_measurement_type(self, value):
        if value not in dict(MenuItem.MEASUREMENT_CHOICES):
            raise serializers.ValidationError("Invalid measurement type")
        return value

# GET / List serializer
class MenuItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'description', 'price', 'measurement_type', 'is_active', 'created_at', 'updated_at']
