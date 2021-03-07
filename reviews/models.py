from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.models import User


class Review(models.Model):
    class StatusReview(models.TextChoices):
        MODERATION = 'new', _('на модерации')
        PUBLISHED = 'published', _('опубликован')
        REJECTED = 'hidden', _('отклонен')

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='my_reviews'
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        default=timezone.now
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=13,
        choices=StatusReview.choices,
        default=StatusReview.MODERATION,
    )
