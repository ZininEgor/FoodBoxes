from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
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
            'address',
        )
        read_only_fields = (
            'username',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['email'].split("@")[0].strip(),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        instance.save()
        return instance
