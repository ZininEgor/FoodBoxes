from django.core.management import BaseCommand
from items.models import Item
import requests

URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/foodboxes.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL).json()
        for item in response:
            Item.objects.get_or_create(
                id=item['id'],
                defaults={
                    'title': item['title'],
                    'description': item['description'],
                    'image': item['image'],
                    'weight': item['weight_grams'],
                    'price': item['price']
                }
            )
        return
