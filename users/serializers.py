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
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
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
        instance.set_email(validated_data['email'])
        instance.set_first_name(validated_data['first_name'])
        instance.set_last_name(validated_data['last_name'])
        instance.set_middle_name(validated_data['middle_name'])
        instance.set_password(validated_data['password'])
        instance.set_phone(validated_data['phone'])
        instance.set_address(validated_data['address'])
        instance.save()
        return instance
