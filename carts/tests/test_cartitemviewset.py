import random
from decimal import Decimal

from django.forms import model_to_dict
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
        cls.url = reverse('carts:CartItem-list')

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.users[0])
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{
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
        } for cart_item in self.cart_items if cart_item.cart == self.users[0].current_cart])


class CartItemViewSetRetrieveTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image="image/small_gif.gif",
                weight=random.randint(0, 10000),
                price=round(random.uniform(2, 10000), 2),

            ) for i in range(21)
        ]
        cls.users = [User.objects.create(
            username=f'egor {i}',
        ) for i in range(2)
        ]
        item_id = random.randint(0, 20)
        cls.cart_item = CartItem.objects.create(
            item=cls.items[item_id],
            cart=cls.users[0].current_cart,
            quantity=random.randint(1, 100),
            price=cls.items[item_id].price,
        )
        cls.url = reverse('carts:CartItem-detail', kwargs={'pk': cls.cart_item.id})

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.users[0])
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': self.cart_item.id,
            'item':
                {'id': self.cart_item.item.id,
                 'title': self.cart_item.item.title,
                 'description': self.cart_item.item.description,
                 'image': "http://testserver" + self.cart_item.item.image.url,
                 'weight': self.cart_item.item.weight,
                 'price': "{:.{}f}".format(self.cart_item.item.price, 2)},
            'quantity': self.cart_item.quantity,
            'item_id': self.cart_item.item_id,
            'price': "{:.{}f}".format(self.cart_item.price, 2),
            'total_price': float("{:.{}f}".format(self.cart_item.total_price, 2)),
        })


class CartItemViewSetUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.item = Item.objects.create(
            title=f'title',
            description=f'description',
            image="image/small_gif.gif",
            weight=random.randint(0, 10000),
            price=round(random.uniform(2, 10000), 2),

        )
        self.user = User.objects.create(
            username=f'egor',
        )

        self.cart_item = CartItem.objects.create(
            item=self.item,
            cart=self.user.current_cart,
            quantity=random.randint(1, 100),
            price=self.item.price,
        )
        self.url = reverse('carts:CartItem-detail', kwargs={'pk': self.cart_item.id})

    def test_put_unauthorized(self):
        response = self.client.put(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_patch_unauthorized(self):
        response = self.client.patch(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_put_quantity(self):
        self.client.force_authenticate(self.user)
        data = {
            "quantity": 0,
            "item_id": 1,
        }
        response = self.client.put(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'quantity': ['Not valid']})

    def test_patch_quantity(self):
        self.client.force_authenticate(self.user)
        data = {
            "quantity": 0,
            "item_id": 1,
        }
        response = self.client.patch(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'quantity': ['Not valid']})

    def test_patch(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, format='json', data={
            "quantity": random.randint(1, 100),
        })
        cart_item = CartItem.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
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
        })
        self.assertEqual(model_to_dict(cart_item), {
            'id': cart_item.id,
            'item': cart_item.item.id,
            'quantity': cart_item.quantity,
            'cart': cart_item.item_id,
            'price': Decimal("{:.{}f}".format(cart_item.price, 2)),
        })

    def test_put(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, format='json', data={
            "quantity": random.randint(1, 100),
        })
        cart_item = CartItem.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "id": cart_item.id,
            "quantity": cart_item.quantity,
            "item_id": cart_item.item.id,
            "total_price": Decimal("{:.{}f}".format(cart_item.total_price, 2)),
        })
        self.assertEqual(model_to_dict(cart_item), {
            'id': cart_item.id,
            'item': cart_item.item.id,
            'quantity': cart_item.quantity,
            'cart': cart_item.item_id,
            'price': Decimal("{:.{}f}".format(cart_item.price, 2)),
        })


class CartItemViewSetDeleteTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.item = Item.objects.create(
            title=f'title',
            description=f'description',
            image="image/small_gif.gif",
            weight=random.randint(0, 10000),
            price=round(random.uniform(2, 10000), 2),

        )
        self.user = User.objects.create(
            username=f'egor',
        )

        self.cart_item = CartItem.objects.create(
            item=self.item,
            cart=self.user.current_cart,
            quantity=random.randint(1, 100),
            price=self.item.price,
        )
        self.url = reverse('carts:CartItem-detail', kwargs={'pk': self.cart_item.id})

    def test_unauthorized(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(CartItem.objects.all()), 0)


class CartItemViewSetCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.user = User.objects.create(
            username=f'egor',
        )
        self.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image="image/small_gif.gif",
                weight=random.randint(0, 10000),
                price=round(random.uniform(2, 10000), 2),

            ) for i in range(21)
        ]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('carts:CartItem-list')

    def test_unauthorized(self):
        response = self.client.post(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_quantity(self):
        self.client.force_authenticate(self.user)
        data = {
            "quantity": 0,
            "item_id": random.randint(1, 20),
        }
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(CartItem.objects.all()), 0)
        self.assertEqual(response.json(), {'quantity': ['Not valid']})

    def test(self):
        self.client.force_authenticate(self.user)
        data = {
            "quantity": random.randint(1, 100),
            "item_id": random.randint(1, 20),
        }
        response = self.client.post(self.url, format='json', data=data)
        cart_item = CartItem.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'id': cart_item.id,
            'item': {
                'id': cart_item.item.id,
                'title': cart_item.item.title,
                'description': cart_item.item.description,
                'image': "http://testserver" + cart_item.item.image.url,
                'weight': cart_item.item.weight,
                'price': "{:.{}f}".format(cart_item.item.price, 2)},
            'quantity': cart_item.quantity,
            'item_id': cart_item.item_id,
            'price': "{:.{}f}".format(cart_item.price, 2),
            'total_price': float("{:.{}f}".format(cart_item.total_price, 2)),
        })
        self.assertEqual(model_to_dict(cart_item), {
            'id': cart_item.id,
            'item': cart_item.item.id,
            'quantity': cart_item.quantity,
            'cart': self.user.current_cart.id,
            'price': Decimal("{:.{}f}".format(cart_item.price, 2)),
        })
