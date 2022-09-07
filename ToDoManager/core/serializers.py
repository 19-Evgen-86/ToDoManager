from django.contrib.auth import password_validation
from django.core.validators import MinLengthValidator
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

class UserDeleteSerialize(serializers.ModelSerializer):
    class Meta:
        model =User
        fields = ["id"]