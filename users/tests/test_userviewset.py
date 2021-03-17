from django.contrib.auth.hashers import make_password
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from users.models import User


class UserViewSetRetrieveTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='egor')

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('users:current')

    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'middle_name': self.user.middle_name,
            'phone': self.user.phone,
            'address': self.user.address,
        })


class UserViewSetUpdateTestCase(APITestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.user = User.objects.create(username='egor', password=make_password('admin123123'))

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('users:current')

    def test_put_unauthorized(self):
        response = self.client.put(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_patch_unauthorized(self):
        response = self.client.patch(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test_put(self):
        data = {
            "email": "user@example.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "middle_name": "middle_name",
            "phone": "phone",
            "address": "address"
        }
        self.client.force_authenticate(self.user)
        response = self.client.put(self.url, format='json', data=data)
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': user.id, 'username': user.username, **data})
        model_dict = model_to_dict(user)
        [model_dict.pop(key) for key in ['groups', 'user_permissions']]
        self.assertEqual(model_dict,
                         {'id': user.id,
                          'password': user.password,
                          'last_login': user.last_login,
                          'is_superuser': user.is_superuser,
                          'username': user.username,
                          'first_name': data['first_name'],
                          'last_name': data['last_name'],
                          'email': data['email'],
                          'is_staff': user.is_staff,
                          'is_active': user.is_active,
                          'date_joined': user.date_joined,
                          'middle_name': data['middle_name'],
                          'phone': data['phone'],
                          'address': data['address']})

    def test_patch(self):
        data = {
            "email": "user@example.com",
            "first_name": "first_name",
            "last_name": "last_name",
            "middle_name": "middle_name",
            "phone": "phone",
            "address": "address"
        }
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.url, format='json', data=data)
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': user.id, 'username': user.username, **data})
        model_dict = model_to_dict(user)
        [model_dict.pop(key) for key in ['groups', 'user_permissions']]
        self.assertEqual(model_dict,
                         {'id': user.id,
                          'password': user.password,
                          'last_login': user.last_login,
                          'is_superuser': user.is_superuser,
                          'username': user.username,
                          'first_name': data['first_name'],
                          'last_name': data['last_name'],
                          'email': data['email'],
                          'is_staff': user.is_staff,
                          'is_active': user.is_active,
                          'date_joined': user.date_joined,
                          'middle_name': data['middle_name'],
                          'phone': data['phone'],
                          'address': data['address']})
