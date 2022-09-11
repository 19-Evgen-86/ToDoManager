from django.contrib.auth import password_validation
from django.core.validators import MinLengthValidator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import serializers

from core.models import User
from core.validators import email_validator


class UserCreateSerialize(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(max_length=150, validators=[MinLengthValidator(1)])
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(validators=[email_validator])
    password = serializers.CharField(min_length=1)
    password_repeat = serializers.CharField(min_length=1)

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        passwd = attrs['password']
        passwd_rep = attrs['password_repeat']
        if passwd != passwd_rep:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class UserDetailSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class UserUpdateSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "username", "first_name", "last_name", "email"]

    def save(self):
        user = super().save()
        return user


class UserUpdatePwdSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["new_password", "old_password"]

    def save(self):

        user = super().save()

        old_password = self.initial_data['old_password']
        new_password = self.initial_data['new_password']

        if not user.check_password(old_password):
            raise serializers.ValidationError("Passwords don't match.")

        if not password_validation.validate_password(new_password):
            raise serializers.ValidationError(errors)

        user.set_password(new_password)
        user.save()
        return user
