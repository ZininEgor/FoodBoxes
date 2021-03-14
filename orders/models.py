from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.models import User


class Order(models.Model):
    class StatusOrder(models.TextChoices):
        CREATED = 'created', _('Создан')
        DELIVERED = 'delivered', _('Доставлен')
        PROCESSED = 'processed', _('В обработке')
        CANCELLED = 'cancelled', _('Отменен')

    created_at = models.DateTimeField(
        default=timezone.now
    )

    delivery_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    recipient = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='orders',
    )

    address = models.CharField(
        max_length=256,
    )

    cart = models.ForeignKey(
        to='carts.Cart',
        on_delete=models.CASCADE,
        related_name='orders',
    )

    status = models.CharField(
        max_length=13,
        choices=StatusOrder.choices,
        default=StatusOrder.CREATED,
    )

    total_cost = models.DecimalField(
        decimal_places=2,
        max_digits=10,
    )
