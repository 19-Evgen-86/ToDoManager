from django.contrib.auth import password_validation, authenticate, login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated
from rest_framework.fields import CurrentUserDefault

from core.models import User


class PasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('write_only', True)
        kwargs['style'] = {'input_type': 'password'}
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class UserCreateSerialize(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ['id', "username", 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs):
        passwd = attrs['password']
        passwd_rep = attrs['password_repeat']
        if passwd != passwd_rep:
            raise ValidationError("Passwords don't match.")

        return attrs

    def create(self, validated_data):
        del validated_data['password_repeat']
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class LoginSerialize(serializers.ModelSerializer):
    password = PasswordField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        if not (user := authenticate(username=username, password=password)):
            raise AuthenticationFailed
        return user


class UserUpdateSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "username", "first_name", "last_name", "email"]


class UserUpdatePwdSerialize(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ['user','old_password','new_password']
    def create(self, validated_data):
        raise NotImplementedError

    def validate(self, attrs):
        old_password = attrs['old_password']
        new_password = attrs['new_password']
        if not (user := attrs['user']):
            raise NotAuthenticated
        if not user.check_password(old_password):
            raise ValidationError({'old_password': 'dont match'})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
