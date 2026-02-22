from rest_framework import serializers
from .models import Category, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    display_price = serializers.CharField(read_only=True)
    has_half_full = serializers.BooleanField(read_only=True)
    image_url     = serializers.SerializerMethodField()

    class Meta:
        model  = MenuItem
        fields = [
            'id',
            'name',
            'description',
            'category',
            'category_name',
            'veg',
            'price_regular',
            'price_half',
            'price_full',
            'display_price',
            'has_half_full',
            'image_url',
            'featured',
            'is_available',
        ]

    def get_image_url(self, obj: MenuItem) -> str | None:
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url


class CategorySerializer(serializers.ModelSerializer):
    """Category with its available items nested."""
    items = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ['id', 'name', 'display_order', 'items']

    def get_items(self, obj):
        available = obj.items.filter(is_available=True)
        return MenuItemSerializer(available, many=True, context=self.context).data


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer — no nested items."""

    class Meta:
        model  = Category
        fields = ['id', 'name', 'display_order']
