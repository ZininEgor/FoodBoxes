from rest_framework import serializers

from reviews.models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'author',
            'status',
            'text',
            'created_at',
            'published_at',
        )
        read_only_fields = (
            'author',
            'status',
            'created_at',
            'published_at',
        )
        extra_kwargs = {
            'text': {
                'required': True
            },
        }
