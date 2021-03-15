from rest_framework import serializers

from carts.serializers import CartSerializer
from orders.models import Order
from users.serializers import UserSerializer


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

    def validate(self, attrs):
        instance = getattr(self, 'instance', None)
        if instance.status != Order.StatusOrder.CREATED.value:
            raise serializers.ValidationError("Impossible to create order without items")
        return attrs


class OrderCreateListSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(
        default=serializers.CurrentUserDefault()
    )

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

    def validate(self, attrs):
        if attrs['recipient'].current_cart.total_cost == 0:
            raise serializers.ValidationError("Impossible to create order without items")
        return attrs

    def create(self, validated_data):
        review = Order(
            recipient=validated_data['recipient'],
            address=validated_data['address'],
            delivery_at=validated_data['delivery_at'],
            cart=validated_data['recipient'].current_cart,
            total_cost=self.validated_data['recipient'].current_cart.total_cost
        )
        review.save()
        return review
