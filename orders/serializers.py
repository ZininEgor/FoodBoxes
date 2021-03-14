from rest_framework import serializers

from carts.serializers import CartSerializer
from orders.models import Order


class OrderRetrieveUpdateSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'cart',
            'status',
            'recipient',
            'total_cost',
            'address',
            'delivery_at',
            'created_at',
        )
        read_only_fields = (
            'cart',
            'recipient',
            'total_cost',
            'created_at',
        )

    def update(self, instance, validated_data):
        if instance.status == 'created':
            instance.status = validated_data.get('status', instance.status)
            instance.address = validated_data.get('address', instance.address)
            instance.delivery_at = validated_data.get('delivery_at', instance.delivery_at)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError(f"It is impossible to change the order as it is {instance.status}")


class OrderCreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'cart',
            'status',
            'total_cost',
            'recipient',
            'address',
            'delivery_at',
            'created_at',
        )
        read_only_fields = (
            'created_at',
            'recipient',
            'cart',
            'total_cost',
            'status',
            'cart',
        )

    def create(self, validated_data):
        if self.context['request'].user.current_cart.total_cost == 0:
            raise serializers.ValidationError("Impossible to create order without items")
        review = Order(
            recipient=self.context['request'].user,
            address=validated_data['address'],
            delivery_at=validated_data['delivery_at'],
            cart=self.context['request'].user.current_cart,
            total_cost=self.context['request'].user.current_cart.total_cost
        )
        review.save()
        self.context['request'].user.create_new_cart()
        return review
