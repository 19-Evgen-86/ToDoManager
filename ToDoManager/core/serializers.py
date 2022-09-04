from rest_framework import serializers

from ToDoManager.core.models import User


class UserCreateSerialize(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = "__all__"


    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(user.password)
        user.save()
        return user
