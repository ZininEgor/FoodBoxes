import random

from django.forms import model_to_dict
from rest_framework import status, serializers
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from reviews.models import Review
from users.models import User


class ReviewViewSetListTestCase(APITestCase):
    def setUp(self) -> None:
        self.status = ['new', 'published', 'hidden']
        self.users = [
            User.objects.create(
                username=f'egor {name}',
            ) for name in range(10)
        ]
        self.reviews = [
            Review.objects.create(
                text=f'text {r}',
                author=random.choice(self.users),
                status=random.choice(self.status),
            ) for r in range(30)
        ]

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('reviews:review-list')

    def test(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), [{
                'id': review.id,
                'author': {
                    'id': review.author.id,
                    'username': review.author.username,
                    'email': review.author.email,
                    'first_name': review.author.first_name,
                    'last_name': review.author.last_name,
                    'middle_name': review.author.middle_name,
                    'phone': review.author.phone,
                    'address': review.author.address,
                },
                'status': review.status,
                'text': review.text,
                'created_at': serializers.DateTimeField().to_representation(review.created_at),
                'published_at': review.published_at
            } for review in self.reviews if review.status == 'published']
        )


class ReviewViewSetCreateTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='egor')
        self.data = {
            'text': 'text',
        }

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('reviews:review-list')

    def test_unauthorized(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

    def test(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=self.data)
        review = Review.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'id': review.id,
            'author': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'middle_name': self.user.middle_name,
                'phone': self.user.phone,
                'address': self.user.address,
            },
            'status': review.status,
            'text': review.text,
            'created_at': serializers.DateTimeField().to_representation(review.created_at),
            'published_at': review.published_at
        })
        self.assertEqual(model_to_dict(review), {
            'id': review.id,
            'author': self.user.id, **self.data,
            'created_at': review.created_at,
            'published_at': review.published_at,
            'status': review.status,
        })
