import random

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from items.models import Item


class ItemViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image="image/small_gif.gif",
                weight=random.randint(0, 10000),
                price=round(random.uniform(0, 10000), 2),

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
            data['results'], [{
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'image': "http://testserver" + item.image.url,
                'weight': item.weight,
                'price': "{:.{}f}".format(item.price, 2),
            } for item in self.items[:len(data['results'])]]
        )


class ItemViewSetRetrieveTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.maxDiff = None
        cls.item = Item.objects.create(
            title=f'title',
            description=f'description',
            image="image/small_gif.gif",
            weight=random.randint(0, 10000),
            price=round(random.uniform(0, 10000), 2),

        )
        cls.url = reverse('items:item-detail', kwargs={'pk': cls.item.id})

    def test(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': self.item.id,
            'title': self.item.title,
            'description': self.item.description,
            'image': "http://testserver" + self.item.image.url,
            'weight': self.item.weight,
            'price': "{:.{}f}".format(self.item.price, 2),
        })
