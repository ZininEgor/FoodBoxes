import datetime

import requests
from django.core.management import BaseCommand
from django.utils.timezone import make_aware

from reviews.models import Review
from users.models import User

URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/reviews.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL).json()
        for review in response:
            try:
                created_at = make_aware(datetime.datetime.strptime(review['created_at'], '%Y-%m-%d'))
            except ValueError:
                created_at = make_aware(datetime.datetime.now())
            try:
                published_at = make_aware(datetime.datetime.strptime(review['published_at'], '%Y-%m-%d'))
            except ValueError:
                published_at = None
            try:
                user = User.objects.get(id=review['author'])
            except User.DoesNotExist:
                user = None
            Review.objects.get_or_create(
                id=review['id'],
                defaults={
                    'author': user,
                    'text': review['content'],
                    'created_at': created_at,
                    'published_at': published_at,
                    'status': review['status']
                }
            )
        return
