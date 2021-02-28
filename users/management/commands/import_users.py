import requests
from users.models import User
from django.core.management import BaseCommand

URL = 'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/recipients.json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(url=URL).json()
        for user in response:
            User.objects.create_user(
                id=user['id'],
                username=user['email'].split("@")[0].strip(),
                email=user['email'],
                password=user['password'],
                first_name=user['info']['name'],
                last_name=user['info']['surname'],
                middle_name=user['info']['patronymic'],
                phone=user['contacts']['phoneNumber'],
                address=user['city_kladr']
            )
        return
