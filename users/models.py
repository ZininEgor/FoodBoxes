from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.contrib.auth.models import AbstractUser

from carts.models import Cart


class User(AbstractUser):
    middle_name = models.CharField(
        max_length=16
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.CharField(
        max_length=64
    )

    @property
    def current_cart(self):
        try:
            cart, _ = Cart.objects.get_or_create(user=self)
        except MultipleObjectsReturned:
            cart = Cart.objects.filter(user=self).all().last()
        return cart

    def create_new_cart(self):
        Cart.objects.create(user=self)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@", 1)[0]
        return super().save(*args, **kwargs)
