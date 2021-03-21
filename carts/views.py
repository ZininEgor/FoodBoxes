from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from carts.models import Cart
from carts.paginators import CartItemPaginator
from carts.serializers import CartSerializer, CartItemSerializer, CartItemUpdateSerializer


class CartViewSet(ReadOnlyModelViewSet):
    serializer_class = CartSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.current_cart


class CartITemViewSet(ModelViewSet):
    pagination_class = CartItemPaginator
    serializer_class = CartItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'update':
            return CartItemUpdateSerializer
        return CartItemSerializer

    def get_queryset(self):
        queryset = Cart.objects.select_related('user').prefetch_related('items').filter(user=self.request.user).first().cart_items.all()
        return queryset
