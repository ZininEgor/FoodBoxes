from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.paginators import OrderPaginator
from orders import serializers


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    pagination_class = OrderPaginator
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return serializers.OrderCreateListSerializer
        return serializers.OrderRetrieveUpdateSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(recipient=self.request.user).all()
        return queryset
