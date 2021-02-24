from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField()
    weight = models.PositiveSmallIntegerField()
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)
