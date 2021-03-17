import random

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from items.models import Item
from items.serializers import ItemSerializer


class ItemViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image=SimpleUploadedFile('small.gif', small_gif, content_type='image/gif'),
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
            data['results'],
            [{
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
