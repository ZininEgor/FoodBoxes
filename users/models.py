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
        cart, _ = Cart.objects.filter(order=False).get_or_create(user=self)
        return cart

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@", 1)[0]
        return super().save(*args, **kwargs)
