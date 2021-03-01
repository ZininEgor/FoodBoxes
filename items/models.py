from django.db import models


class Item(models.Model):
    title = models.CharField(
        max_length=128
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to='items'
    )

    weight = models.PositiveSmallIntegerField()

    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
    )
