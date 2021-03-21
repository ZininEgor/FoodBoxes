import random
from decimal import Decimal

from django.forms import model_to_dict
from rest_framework import status, serializers
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from carts.models import CartItem
from items.models import Item
from orders.models import Order
from users.models import User


class CartItemViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image=None,
                weight=random.randint(0, 10000),
                price=round(random.uniform(2, 10000), 2),

            ) for i in range(21)
        ]
        self.users = [
            User.objects.create(
                username=f'egor {i}',
            ) for i in range(2)
        ]
        self.orders = []
        for i in range(0, 10):
            self.cart_items = [
                CartItem.objects.create(
                    item=self.items[i],
                    cart=self.users[0].current_cart,
                    quantity=random.randint(1, 100),
                    price=self.items[i].price,
                ) for i in range(5)
            ]
            self.orders.append(Order.objects.create(
                recipient=self.users[0],
                address=f'address {random.randint(0, 100)}',
                cart=self.users[0].current_cart,
                total_cost=self.users[0].current_cart.total_cost,
            ))

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('orders:order-list')

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.users[0])
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'id': order.id,
             'cart': order.cart.id,
             'status': Order.StatusOrder.CREATED.value,
             'total_cost': str("{:.{}f}".format(order.total_cost, 2)),
             'recipient': {
                 'id': self.users[0].id,
                 'username': self.users[0].username,
                 'email': self.users[0].email,
                 'first_name': self.users[0].first_name,
                 'last_name': self.users[0].last_name,
                 'middle_name': self.users[0].middle_name,
                 'phone': self.users[0].phone,
                 'address': self.users[0].address},
             'address': order.address,
             'delivery_at': order.delivery_at,
             'created_at': serializers.DateTimeField().to_representation(order.created_at),
             } for order in self.orders
        ])


class CartItemViewSetRetrieveTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image='image/small.gif',
                weight=random.randint(0, 10000),
                price=round(random.uniform(2, 10000), 2),

            ) for i in range(21)
        ]
        self.user = User.objects.create(username=f'egor', )
        self.cart_items = [
            CartItem.objects.create(
                item=self.items[i],
                cart=self.user.current_cart,
                quantity=random.randint(1, 100),
                price=self.items[i].price,
            ) for i in range(10)
        ]
        self.order = (Order.objects.create(
            recipient=self.user,
            address=f'address {random.randint(0, 100)}',
            cart=self.user.current_cart,
            total_cost=self.user.current_cart.total_cost,
        ))
        self.url = reverse('orders:order-detail', kwargs={'pk': self.order.id})

    def test_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order = Order.objects.get()
        self.assertEqual(response.json(),
                         {
                             'id': order.id,
                             'cart': {
                                 'id': order.cart.id,
                                 'items': [{
                                     'id': cart_items.id,
                                     'item':
                                         {'id': cart_items.item.id,
                                          'title': cart_items.item.title,
                                          'description': cart_items.item.description,
                                          'image': 'http://testserver' + cart_items.item.image.url,
                                          'weight': cart_items.item.weight,
                                          'price': str("{:.{}f}".format(cart_items.item.price, 2))},
                                     'quantity': cart_items.quantity,
                                     'item_id': cart_items.item.id,
                                     'price': str("{:.{}f}".format(cart_items.item.price, 2)),
                                     'total_price': float("{:.{}f}".format(cart_items.total_price, 2)),
                                 } for cart_items in self.cart_items],
                                 'total_cost': float("{:.{}f}".format(order.total_cost, 2))},
                             'status': order.StatusOrder.CREATED.value,
                             'recipient': order.recipient.id,
                             'total_cost': str("{:.{}f}".format(order.total_cost, 2)),
                             'address': order.address,
                             'delivery_at': order.delivery_at,
                             'created_at': serializers.DateTimeField().to_representation(order.created_at)
                         }
                         )


class CartItemViewSetUpdateTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image='image/small.gif',
                weight=random.randint(0, 10000),
                price=round(random.uniform(2, 10000), 2),

            ) for i in range(21)
        ]
        self.user = User.objects.create(username=f'egor', )
        self.cart_items = [
            CartItem.objects.create(
                item=self.items[i],
                cart=self.user.current_cart,
                quantity=random.randint(1, 100),
                price=self.items[i].price,
            ) for i in range(10)
        ]
        self.order = (Order.objects.create(
            recipient=self.user,
            address=f'address {random.randint(0, 100)}',
            cart=self.user.current_cart,
            total_cost=self.user.current_cart.total_cost,
        ))
        self.url = reverse('orders:order-detail', kwargs={'pk': self.order.id})

    def test_put_unauthorized(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_patch_unauthorized(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_status_order(self):
        self.client.force_authenticate(self.user)
        order = Order.objects.get()
        order.status = Order.StatusOrder.PROCESSED
        order.save()
        data = {
            "status": Order.StatusOrder.CANCELLED,
            "address": "Pushkova",
            "delivery_at": "2021-03-21T18:12:42.619Z"
        }
        response = self.client.put(self.url, format='json', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Impossible to change this item']})

    def test_put(self):
        self.client.force_authenticate(self.user)
        data = {
            "status": Order.StatusOrder.CANCELLED,
            "address": "Pushkova",
            "delivery_at": "2021-03-21T18:12:42.619Z"
        }
        response = self.client.put(self.url, format='json', data=data)
        order = Order.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(model_to_dict(order), {
            'id': order.id,
            'created_at': order.created_at,
            'delivery_at': order.delivery_at,
            'recipient': order.recipient.id,
            'address': order.address,
            'cart': order.cart.id,
            'status': Order.StatusOrder.CANCELLED.value,
            'total_cost': Decimal(order.total_cost)
        })

        self.assertEqual(response.json(), {
            'id': order.id,
            'cart': {
                'id': order.cart.id,
                'items': [{
                    'id': cart_items.id,
                    'item':
                        {'id': cart_items.item.id,
                         'title': cart_items.item.title,
                         'description': cart_items.item.description,
                         'image': 'http://testserver' + cart_items.item.image.url,
                         'weight': cart_items.item.weight,
                         'price': str("{:.{}f}".format(cart_items.item.price, 2))},
                    'quantity': cart_items.quantity,
                    'item_id': cart_items.item.id,
                    'price': str("{:.{}f}".format(cart_items.item.price, 2)),
                    'total_price': float("{:.{}f}".format(cart_items.total_price, 2)),
                } for cart_items in self.cart_items],
                'total_cost': float("{:.{}f}".format(order.total_cost, 2))},
            'status': order.StatusOrder.CANCELLED.value,
            'recipient': order.recipient.id,
            'total_cost': str("{:.{}f}".format(order.total_cost, 2)),
            'address': order.address,
            'delivery_at': serializers.DateTimeField().to_representation(order.delivery_at),
            'created_at': serializers.DateTimeField().to_representation(order.created_at)
        })

    def test_patch(self):
        self.client.force_authenticate(self.user)
        data = {
            "status": Order.StatusOrder.CANCELLED,
            "address": "Pushkova",
            "delivery_at": "2021-03-21T18:12:42.619Z"
        }
        response = self.client.patch(self.url, format='json', data=data)
        order = Order.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(model_to_dict(order), {
            'id': order.id,
            'created_at': order.created_at,
            'delivery_at': order.delivery_at,
            'recipient': order.recipient.id,
            'address': order.address,
            'cart': order.cart.id,
            'status': Order.StatusOrder.CANCELLED.value,
            'total_cost': Decimal(order.total_cost)
        })

        self.assertEqual(response.json(), {
            'id': order.id,
            'cart': {
                'id': order.cart.id,
                'items': [{
                    'id': cart_items.id,
                    'item':
                        {'id': cart_items.item.id,
                         'title': cart_items.item.title,
                         'description': cart_items.item.description,
                         'image': 'http://testserver' + cart_items.item.image.url,
                         'weight': cart_items.item.weight,
                         'price': str("{:.{}f}".format(cart_items.item.price, 2))},
                    'quantity': cart_items.quantity,
                    'item_id': cart_items.item.id,
                    'price': str("{:.{}f}".format(cart_items.item.price, 2)),
                    'total_price': float("{:.{}f}".format(cart_items.total_price, 2)),
                } for cart_items in self.cart_items],
                'total_cost': float("{:.{}f}".format(order.total_cost, 2))},
            'status': order.StatusOrder.CANCELLED.value,
            'recipient': order.recipient.id,
            'total_cost': str("{:.{}f}".format(order.total_cost, 2)),
            'address': order.address,
            'delivery_at': serializers.DateTimeField().to_representation(order.delivery_at),
            'created_at': serializers.DateTimeField().to_representation(order.created_at)
        })


class CartItemViewSetCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.items = [
            Item.objects.create(
                title=f'title',
                description=f'description {i}',
                image='image/small.gif',
                weight=random.randint(0, 10000),
                price=round(random.uniform(2, 10000), 2),

            ) for i in range(21)
        ]
        self.user = User.objects.create(username=f'egor', )
        self.cart_items = [
            CartItem.objects.create(
                item=self.items[i],
                cart=self.user.current_cart,
                quantity=random.randint(1, 100),
                price=self.items[i].price,
            ) for i in range(10)
        ]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('orders:order-list')

    def test_total_cost(self):
        self.client.force_authenticate(self.user)
        data = {
            "address": "Pushkina",
            "delivery_at": "2021-03-21T18:57:53.256Z"
        }
        self.client.post(self.url, data=data)
        data = {
            "address": "Pushkina",
            "delivery_at": "2021-03-21T18:57:53.256Z"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Impossible to create order without items']})


    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        data = {
            "address": "Pushkina",
            "delivery_at": "2021-03-21T18:57:53.256Z"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get()
        self.assertEqual(model_to_dict(order), {
            'id': order.id,
            'created_at': order.created_at,
            'delivery_at': order.delivery_at,
            'recipient': order.recipient.id,
            'address': order.address,
            'cart': order.cart.id,
            'status': Order.StatusOrder.CREATED.value,
            'total_cost': Decimal(order.total_cost)
        })
        self.assertEqual(response.json(), {
            'id': order.id,
            'cart': order.cart.id,
            'status': Order.StatusOrder.CREATED.value,
            'total_cost': str(order.total_cost),
            'recipient': {
                'id': order.recipient.id,
                'username': order.recipient.username,
                'email': order.recipient.email,
                'first_name': order.recipient.first_name,
                'last_name': order.recipient.last_name,
                'middle_name': order.recipient.middle_name,
                'phone': order.recipient.phone,
                'address': order.recipient.address,
            },
            'address': order.address,
            'delivery_at': serializers.DateTimeField().to_representation(order.delivery_at),
            'created_at': serializers.DateTimeField().to_representation(order.created_at)})
