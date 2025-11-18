from rest_framework import serializers
from .models import Restaurant

# ======================
# Create serializer
# ======================
class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'is_active']

    def validate_name(self, value):
        if Restaurant.objects.filter(name=value).exists():
            raise serializers.ValidationError("This restaurant name is already taken.")
        return value


# ======================
# Update serializer
# ======================
class RestaurantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'is_active']

    def validate_name(self, value):
        # Update paytida boshqa restaurant nomi bilan to'qnashmasligi
        if Restaurant.objects.filter(name=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("This restaurant name is already taken.")
        return value


# ======================
# List serializer
# ======================
class RestaurantListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'owner', 'is_active', 'created_at', 'updated_at']


# ======================
# Delete serializer
# ======================
class RestaurantDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id']
