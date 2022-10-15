from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated

from core.models import User


class PasswordField(serializers.CharField):
    """
    сериализатор для пароля
    """

    def __init__(self, **kwargs):
        kwargs.setdefault('write_only', True)
        kwargs['style'] = {'input_type': 'password'}
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class UserCreateSerialize(serializers.ModelSerializer):
    """
      сериализатор для создания пользователя
    """
    password: str = PasswordField(required=True)
    password_repeat: str = PasswordField(required=True)

    class Meta:
        model = User
        fields = ['id', "username", 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs):
        passwd: str = attrs['password']
        passwd_rep: str = attrs['password_repeat']
        if passwd != passwd_rep:
            raise ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        del validated_data['password_repeat']
        user: User = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class LoginSerialize(serializers.ModelSerializer):
    """
    сериализатор для авторизации пользователя
    """
    password: str = PasswordField(required=True)
    username: str = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", 'password']

    def create(self, validated_data):
        username: str = validated_data['username']
        password: str = validated_data['password']

        if not (user := authenticate(username=username, password=password)):
            raise AuthenticationFailed
        return user


class UserUpdateSerialize(serializers.ModelSerializer):
    """
       сериализатор для обновления пользователя
       """

    class Meta:
        model = User
        fields = ['id', "username", "first_name", "last_name", "email"]


class UserUpdatePwdSerialize(serializers.ModelSerializer):
    """
       сериализатор для обновления пароля пользователя
    """
    user: User = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password: str = PasswordField(required=True)
    new_password: str = PasswordField(required=True)

    class Meta:
        model = User
        fields = ['user', 'old_password', 'new_password']

    def create(self, validated_data):
        raise NotImplementedError

    def validate(self, attrs):
        old_password: str = attrs['old_password']
        if not (user := attrs['user']):
            raise NotAuthenticated
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'dont match'})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
