from django.forms import model_to_dict
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User


class UserCreateTestCase(APITestCase):

    def setUp(self) -> None:
        self.data = {
            'email': 'user@example.com',
            'password': 'admin123123',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'middle_name': 'middle_name',
            'phone': 'phone',
            'address': 'address'
        }

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('users:register')

    def test(self):
        response = self.client.post(self.url, data=self.data)
        user = User.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(model_to_dict(user),
                         {'id': user.id,
                          'password': user.password,
                          'last_login': user.last_login,
                          'is_superuser': user.is_superuser,
                          'username': user.username,
                          'first_name': self.data['first_name'],
                          'last_name': self.data['last_name'],
                          'email': self.data['email'],
                          'is_staff': user.is_staff,
                          'is_active': user.is_active,
                          'date_joined': user.date_joined,
                          'middle_name': self.data['middle_name'],
                          'phone': self.data['phone'],
                          'address': self.data['address'],
                          'groups': list(user.groups.all()),
                          'user_permissions': list(user.user_permissions.all()),
                          })
        self.data.pop('password')
        self.assertEqual(response.json(), {'id': user.id, 'username': user.username, **self.data})
