from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Item


@api_view(['GET'])
def get_item_view(request, pk, *args, **kwargs):
    item = get_object_or_404(Item, pk=pk)
    return Response({
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'image': item.image.url,
        'weight': item.weight,
        'price': str(item.price),
    })
