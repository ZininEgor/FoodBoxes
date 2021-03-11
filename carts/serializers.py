from rest_framework import serializers

from carts.models import Cart, CartItem
from items.models import Item
from items.serializers import ItemSerializer


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            'id',
            'quantity',
            'item_id',
            'total_price',
        )
        read_only_fields = (
            'price',
            'total_price',
            'item_id',
        )
        extra_kwargs = {
            'quantity': {
                'required': True
            },
        }

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Not valid")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        source='item',
        queryset=Item.objects.all(),
    )

    class Meta:
        model = CartItem
        fields = (
            'id',
            'item',
            'quantity',
            'item_id',
            'price',
            'total_price',
        )
        read_only_fields = (
            'price',
            'total_price',
            'item',
        )
        extra_kwargs = {
            'quantity': {
                'required': True
            },
        }

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Not valid")
        return value

    def create(self, validated_data):
        cart_item = CartItem(
            item=validated_data['item'],
            cart=self.context['request'].user.current_cart,
            quantity=validated_data['quantity'],
            price=validated_data['item'].price,
        )
        cart_item.save()
        return cart_item


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cart_items', many=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'items',
            'total_cost',
        )
