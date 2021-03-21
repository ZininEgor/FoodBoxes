import json

from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from items.filters import ItemFilter
from items.models import Item
from items.paginators import ItemPaginator
from items.serializers import ItemSerializer

ITEMS_CACHE_KEY = 'items_cache_key_{}'
ITEMS_CACHE_TTL = 60


class ItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemPaginator
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ItemFilter
    ordering_fields = ['price', 'id']

    def list(self, request, *args, **kwargs):
        key = ITEMS_CACHE_KEY.format(request.GET.get('page'))
        cached_response = cache.get(key)
        if cached_response:
            return Response(json.loads(cached_response), status=status.HTTP_200_OK)
        response = super().list(request, *args, **kwargs)
        cache.set(key, json.dumps(response.data), ITEMS_CACHE_TTL)
        return response
