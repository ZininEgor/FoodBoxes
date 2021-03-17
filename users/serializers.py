from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'middle_name',
            'phone',
            'address'
        )
        read_only_fields = ('username',)

    def validated_password(self, value):
        validate_password(value)
        return make_password(value)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'phone',
            'address',
        )
        read_only_fields = ('username',)
