import random

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from carts.models import CartItem
from items.models import Item
from users.models import User


class CartItemViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image="image/small_gif.gif",
                weight=random.randint(0, 10000),
                price=round(random.uniform(2, 10000), 2),

            ) for i in range(21)
        ]
        self.users = [User.objects.create(
            username=f'egor {i}',
        ) for i in range(2)
        ]
        self.cart_items = [
            CartItem.objects.create(
                item=self.items[i],
                cart=random.choice(self.users).current_cart,
                quantity=random.randint(1, 100),
                price=self.items[i].price,
            ) for i in range(10)
        ]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('carts:cart-list')

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.users[0])
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), {
                'id': self.users[0].current_cart.id,
                'items': [{
                    'id': cart_item.id,
                    'item':
                        {'id': cart_item.item.id,
                         'title': cart_item.item.title,
                         'description': cart_item.item.description,
                         'image': "http://testserver" + cart_item.item.image.url,
                         'weight': cart_item.item.weight,
                         'price': "{:.{}f}".format(cart_item.item.price, 2)},
                    'quantity': cart_item.quantity,
                    'item_id': cart_item.item_id,
                    'price': "{:.{}f}".format(cart_item.price, 2),
                    'total_price': float("{:.{}f}".format(cart_item.total_price, 2)),
                } for cart_item in self.cart_items if cart_item.cart == self.users[0].current_cart],
                'total_cost': float(self.users[0].current_cart.total_cost),
            }

        )
