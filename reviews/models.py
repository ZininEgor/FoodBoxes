from django.db import models
from users.models import User


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField()
    published_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=13)
