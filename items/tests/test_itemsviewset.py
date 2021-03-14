from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from items.models import Item
from items.serializers import ItemSerializer


class ItemViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image=None,
                weight=i,
                price=i,

            ) for i in range(12)
        ]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('items:item-list')

    def test(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(
            data['results'],
            [ItemSerializer(item).data for item in self.items[:len(data['results'])]]
        )


class ItemViewSetRetrieveTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(
            title=f'title',
            description=f'description',
            image=None,
            weight=120,
            price=2500,
        )
        cls.url = reverse('items:item-detail', kwargs={'pk': cls.item.id})

    def test(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            ItemSerializer(self.item).data
        )
