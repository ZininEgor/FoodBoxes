from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


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


@receiver([post_save, post_delete])
def invalidate_items_cache(sender, instance, **kwargs):
    from items.views import ITEMS_CACHE_KEY

    cache.delete(ITEMS_CACHE_KEY)
