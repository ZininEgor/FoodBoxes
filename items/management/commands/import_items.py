import requests
from items.models import Item
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management import BaseCommand

URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/foodboxes.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL).json()
        for item in response:
            item_created, created = Item.objects.get_or_create(
                id=item['id'],
                defaults={
                    'title': item['title'],
                    'description': item['description'],
                    'image': item['image'],
                    'weight': item['weight_grams'],
                    'price': item['price']
                }
            )
            if created:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(urlopen(item['image']).read())
                img_temp.flush()
                item_created.image.save(f"foodb{item_created.pk}", File(img_temp))
        return
